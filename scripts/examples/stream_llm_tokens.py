from pydantic import BaseModel, Field
from typing import Dict, Sequence, Annotated
from typing_extensions import TypedDict
import operator

from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph import END, StateGraph

from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()


class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")


model = ChatOllama(
    streaming=True,
    model="llama3.1",
    temperature=0,
).with_structured_output(Joke)


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


async def agenerate(
    state: GraphState,
    config: RunnableConfig
) -> Dict:
    """
    Generates a response.

    Args:
        state (messages): The current state of the agent.
    Returns:
        dict: The output key is filled.
    """

    output = await model \
        .ainvoke(
            state['messages'],
            config=config
        )

    return {'messages': [output]}

# Graph
graph = StateGraph(GraphState)

graph.add_node('model', agenerate)
graph.set_entry_point('model')
graph.add_edge('model', END)

# Compile
compiled_graph = graph.compile()


async def run_model():

    async for event in model.astream_events(
        [HumanMessage("tell me a joke about giraffas")],
        version='v2'
    ):

        print(event['event'])


async def run_graph():
    async for event in compiled_graph.astream_events(
        {'messages': [HumanMessage("tell me a joke about giraffas")]},
        version='v2'
    ):
        # print(event['event'])
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(event)
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI or Anthropic usually means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")

if __name__ == '__main__':

    import asyncio

    print("Running model")
    asyncio.run(run_model())
    print("\n\n----------------\n\n")
    print("Running graph")
    asyncio.run(run_graph())
