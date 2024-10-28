from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache
import os


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class AppSettings(BaseSettings):
    api_version: Optional[str] = None
    api_name: Optional[str] = None
    api_key: Optional[str] = None
    debug_mode: Optional[str] = None
    tavily_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    ehrs_api_key: Optional[str] = None
    ehrs_endpoint: Optional[str] = None
    terminology_endpoint: Optional[str] = None
    terminology_api_key: Optional[str] = None
    fhir_endpoint: Optional[str] = None
    groq_api_key: Optional[str] = None
    groq_model: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=get_env_filename(), env_file_encoding="utf-8")


settings = AppSettings()


@lru_cache()
def get_app_settings():
    return AppSettings()
