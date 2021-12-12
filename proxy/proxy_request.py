import re
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, validator


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class ProxyRequest(BaseModel):
    method: RequestMethod
    domain: str
    endpoint: str
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, str]] = None

    @validator("endpoint")
    def validate_endpoint(cls, endpoint):
        assert not not re.match(r"^\/[\S]*$", endpoint), "Invalid endpoint"
        return endpoint
