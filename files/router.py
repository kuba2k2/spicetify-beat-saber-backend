import os
from os.path import dirname, isdir, isfile

from fastapi import APIRouter

from .files_response import FilesResponse

router = APIRouter(prefix="/files", tags=["File management"])


@router.get("/")
async def files_list(path: str):
    path = path or "/"
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
            parent="",
            dirs=drives,
            files=[],
        )

    path = path.strip("/\\")
    path = path.replace("/", os.sep).replace("\\", os.sep)
    path += os.sep
    parent = dirname(dirname(path))

    if isfile(path):
        raise ValueError("path is a file")
    if not isdir(path):
        raise ValueError("path does not exist")

    (_, dirs, files) = next(os.walk(path))
    return FilesResponse(
        path=path,
        parent=parent if path != parent else "",
        dirs=sorted(dirs, key=lambda x: x.lower()),
        files=sorted(files, key=lambda x: x.lower()),
    )
