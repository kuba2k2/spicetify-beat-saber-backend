from fastapi import HTTPException, Request, status

from levels.level_manager import LevelManager


async def level_manager() -> LevelManager:
    return LevelManager.get_instance()


async def authenticate(request: Request):
    if request.client.host != "127.0.0.1":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
