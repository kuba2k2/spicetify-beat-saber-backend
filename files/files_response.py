from typing import List

from pydantic import BaseModel


class FilesResponse(BaseModel):
    path: str
    dirs: List[str]
    files: List[str]
    pathsep: str
