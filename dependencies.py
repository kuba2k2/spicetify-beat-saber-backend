import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from levels.level_manager import LevelManager
from settings import Settings

settings = Settings()
security = HTTPBasic()


async def level_manager() -> LevelManager:
    return LevelManager.get_instance()


async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    valid_username = secrets.compare_digest(
        credentials.username, settings.auth_username
    )
    valid_password = secrets.compare_digest(
        credentials.password, settings.auth_password
    )
    if not (valid_username and valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
