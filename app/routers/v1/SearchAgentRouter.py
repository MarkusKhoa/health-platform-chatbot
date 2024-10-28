from fastapi import APIRouter, Depends, HTTPException
from app.schemas.SearchAgentSchema import SearchAgentQuestionSchema, SearchAgentAnswerSchema
from app.schemas.CommonSchema import CommonResponse
from app.agents.search_agent.agent import search_agent
from scripts.retrievers.lab_codes_retriever import search_lab_codes

SearchAgentRouter = APIRouter(
    prefix="/v1/search-agent", tags=["search-agent"]
)


@SearchAgentRouter.get("")
def hello_world():
    return search_lab_codes("thí nghiệm")


@SearchAgentRouter.post("/chat/{thread_id}", response_model=CommonResponse[str])
def chat_search_agent(thread_id: str, payload: SearchAgentQuestionSchema):
    config = {"configurable": {"thread_id": thread_id}}
    answer = search_agent.run(question=payload.question, config=config)
    return CommonResponse[str](
        data=answer
    )
