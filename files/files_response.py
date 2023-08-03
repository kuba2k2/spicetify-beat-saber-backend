from typing import List

from pydantic import BaseModel


class FilesResponse(BaseModel):
    path: str
    parent: str
    dirs: List[str]
    files: List[str]
