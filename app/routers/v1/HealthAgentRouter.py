from fastapi import APIRouter, Depends, HTTPException
from app.schemas.HealthAgentSchema import HealthAgentAnswerSchema, HealthAgentQuestionSchema
from app.schemas.CommonSchema import CommonResponse
from app.agents.health_agent.agent import ehr_chatbot
from app.utils.db_helpers import check_patient_id
from app.core.auth import get_api_key
from scripts.retrievers.lab_codes_retriever import search_lab_codes
from typing import List
import requests
import os

HealthAgentRouter = APIRouter(
    prefix="/v1/health-agent", tags=["health-agent"]
)


@HealthAgentRouter.get("/labs/search", response_model=CommonResponse[List[str]], dependencies=[Depends(get_api_key)])
def search_labs(lab_name: str):
    lab_codes = search_lab_codes(lab_name=lab_name)
    return CommonResponse[List[str]](
        data=lab_codes
    )


# @HealthAgentRouter.post("/chat", response_model=CommonResponse[str], dependencies=[Depends(get_api_key)])
def chat_search_agent(message):
    # if check_patient_id(payload.patient_id) is False:
    #     raise HTTPException(status_code=404, detail="Patient ID invalid")
    
    config = {
        "configurable": {
            "thread_id": "1"
            #"patient_id": payload.patient_id
        }
    }
    response = ehr_chatbot.invoke(
        {"messages": [("human", message)]}, config=config)
    # answer = response["messages"][-1].content
    combined_answer = " ".join(msg.content for msg in response["messages"])
    return CommonResponse[str](
        data=combined_answer
    )