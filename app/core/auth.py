from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from fastapi import status
from app.config.AppSettings import get_app_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    app_settings = get_app_settings()
    if api_key_header == app_settings.api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please include a valid API key in your request headers."
        )
