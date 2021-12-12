from typing import Dict, List, Union

from pydantic import BaseModel


class ProxyResponse(BaseModel):
    domain: str
    url: str
    headers: Dict[str, Union[str, List[str]]]
    status: int
    body: str
