from dotenv import load_dotenv
from typing import TypedDict, Sequence, Annotated, List
from pydantic import BaseModel, Field
from loguru import logger
from langchain_core.messages import SystemMessage, AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.managed import IsLastStep
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph, MessageGraph   
from langchain_openai import ChatOpenAI
from scripts.tools.encounter_tools import fetch_recent_encounters, search_encounters
from scripts.tools.patient_tools import get_patient_information
from scripts.tools.lab_result_tools import search_lab_results
from scripts.tools.vital_sign_tools import search_vital_signs
from scripts.tools.medication_tools import search_medicines
from app.config.AppSettings import get_app_settings

app_settings = get_app_settings()
MAX_LAST_MESSAGES = 3

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    is_last_step: IsLastStep

# Initialize LLM model and members in graph
members = ["agent", "reflection_agent"]

model = ChatOpenAI(model=app_settings.openai_model,
                   api_key=app_settings.openai_api_key, temperature=0)

supervisor_prompt = SystemMessage(content="""You are the supervisor who can analyze the user question.
                                  You can determine if the user is asking medical questions or not.
                                  If there is no absolute keyword relating to medical domain, deny to answer.""")

medical_expert_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert AI assistant on medical domain. You can answer patients' questions based on the tools you are provided. 
            Your role is determined to be a supervisor for your tools. Once you are given an input question, you can assign which tools
            of yours to retrieve information and help you answer. Therefore, you must do these actions as follows to demonstrate your reasoning steps:
    
            1. Based on the given context, question. You must firstly announce that you are assigning which possible tools to help you
            look up information. That's the first and only thing you need to do at this time.
            2. Remember to mention the exact name of the tools below, too. It helps us to track which tools more easily.
            3. You must notice that many possible tools can be activated to help you look up information at the time you receive question.
            
            However, you are not allowed to answer questions about how to cure diseases or prescribe medications for patients yourself.
            If you detect the violation, you must also notify to the users. You must also deny to answer non-medical related questions.
            """
        )
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a tool chosen reviewer. Analyze, critique and recommendations based on medical context."
            """Provide detailed recommendations and explanation if you found that the agent choose wrong tools. 
            Remember to mention the exact name of the tools when you review the decsion of the previous agent.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
reflect_agent = reflection_prompt | model


tools = [
    get_patient_information,
    fetch_recent_encounters,
    search_encounters,
    search_lab_results,
    search_vital_signs,
    search_medicines
]
medical_model = model.bind_tools(tools)
memory = MemorySaver()

def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return "end"
    if any(isinstance(msg, AIMessage) for msg in state):
        return "reflection"
    return "end"


# def should_continue(state: AgentState):
#     messages = state["messages"]
#     last_message = messages[-1]
#     # If there is no function call, then we finish
#     if not last_message.tool_calls:
#         return "end"
#     else:
#         return "reflection"

def get_modified_messages(state: AgentState, config: RunnableConfig) -> List[BaseMessage]:
    # TODO: get history messages based on thread_id and patient_id
    # configuration = config.get("configurable", {})
    # thread_id = configuration.get("thread_id", None)
    # last_messages = message_history.get_messages_by_session_id(thread_id)
    count = 0
    break_point = 0
    for i in range(len(state["messages"]) - 1):
        index = len(state["messages"]) - 1 - i
        message = state["messages"][index]
        if isinstance(message, HumanMessage):
            count += 1
        if count == MAX_LAST_MESSAGES:
            break_point = index - len(state["messages"])
            break
    expert_messages = medical_expert_prompt.format_messages()
    supervisor_messages = [supervisor_prompt]
    messages = expert_messages +  supervisor_messages + state["messages"][break_point:]
    return messages

async def reflection_node(messages: Sequence[BaseMessage]):
    translated = [medical_expert_prompt] + [
        HumanMessage(content=msg.content) if msg.type == "ai" else AIMessage(content=msg.content)
        for msg in messages[1:]
    ]
    response = await reflect_agent.ainvoke({"messages": translated})
    logger.info("Reflection message: {}".format(response))
    reflection_message = HumanMessage(content=response.content)
    return {"reflection_messages": [reflection_message]}

def call_model(
    state: AgentState,
    config: RunnableConfig,
):
    # TODO: We can modify messages (delete, filter messages) to reduce input token before invoking llm model
    response = medical_model.invoke(get_modified_messages(state, config), config)
    if state["is_last_step"] and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


async def acall_model(state: AgentState, config: RunnableConfig):
    # TODO: We can modify messages (delete, filter messages) to reduce input token before invoking llm model
    response = await medical_model.ainvoke(get_modified_messages(state, config), config)
    if state["is_last_step"] and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    messages = [response]
    if "reflection_messages" in state:
        messages.extend(state["reflection_messages"])
    
    return {"messages": messages}
    # return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", RunnableLambda(call_model, acall_model))
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("reflection", RunnableLambda(reflection_node))

workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
workflow.set_entry_point("agent")
workflow.add_edge("tools", "reflection")
workflow.add_edge("reflection", "agent")

ehr_chatbot = workflow.compile(
    checkpointer=memory,
    debug=False,
)
