import os
from os.path import isdir, isfile, join

from fastapi import APIRouter

from .files_response import FilesResponse

router = APIRouter(prefix="/files", tags=["File management"])


@router.post("/")
async def files_list(path: str):
    if path == "/" and os.name == "nt":
        import string
        from ctypes import windll

        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:")
            bitmask >>= 1
        return FilesResponse(
            path="",
            dirs=drives,
            files=[],
            pathsep=os.sep,
        )

    path = path.replace("/", os.sep).replace("\\", os.sep)

    if isfile(path):
        raise ValueError("path is a file")
    if not isdir(path):
        raise ValueError("path does not exist")

    (_, dirs, files) = next(os.walk(join(path, "")))
    return FilesResponse(
        path=path.rstrip("/\\"),
        dirs=sorted(dirs),
        files=sorted(files),
        pathsep=os.sep,
    )
