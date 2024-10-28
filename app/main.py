from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.AppSettings import get_app_settings
from dotenv import load_dotenv
from app.routers.v1.HealthAgentRouter import HealthAgentRouter

load_dotenv()
app_settings = get_app_settings()

app = FastAPI(
    title=app_settings.api_name,
    version=app_settings.api_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(HealthAgentRouter)
