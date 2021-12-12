from io import BytesIO

from fastapi import APIRouter, Depends
from httpx import AsyncClient

from dependencies import level_manager

from .level_manager import LevelManager

router = APIRouter(prefix="/levels", tags=["Level management"])


@router.get("/hashes")
async def levels_hashes(lmgr: LevelManager = Depends(level_manager)):
    return [level.hash for level in lmgr.levels]


@router.get("/")
async def levels(lmgr: LevelManager = Depends(level_manager)):
    return lmgr.levels


@router.get("/download/{hash}")
async def levels_download(hash: str, lmgr: LevelManager = Depends(level_manager)):
    async with AsyncClient() as client:
        url = f"https://cdn.beatsaver.com/{hash}.zip"
        response = await client.get(url)
        disposition = response.headers["content-disposition"]
        filename = disposition.partition("filename=")[2].strip('"')
        level_dir = filename.rpartition(".zip")[0]
        if not level_dir:
            raise ValueError("Content disposition is invalid")
        return lmgr.save_level(level_dir, BytesIO(response.read()))


@router.get("/delete/{level_dir}")
async def levels_delete(level_dir: str, lmgr: LevelManager = Depends(level_manager)):
    lmgr.delete_level(level_dir)
    return ""
