from fastapi import APIRouter
from httpx import AsyncClient

from .proxy_request import ProxyRequest, RequestMethod
from .proxy_response import ProxyResponse

router = APIRouter(prefix="/proxy", tags=["bsaber.com proxy"])


@router.post("/", response_model=ProxyResponse)
async def bsaber_proxy(request: ProxyRequest):
    async with AsyncClient() as client:
        url = "https://" + request.domain + request.endpoint
        if request.method == RequestMethod.GET:
            response = await client.get(url, headers=request.headers, timeout=60)
        elif request.method == RequestMethod.POST:
            response = await client.post(
                url,
                data=request.params,
                headers=request.headers,
                follow_redirects=False,
                timeout=60,
            )

        headers = dict(response.headers.items())
        if "set-cookie" in headers:
            headers["set-cookie"] = response.headers.get_list("set-cookie")

        return ProxyResponse(
            domain=request.domain,
            url=url,
            headers=headers,
            status=response.status_code,
            body=response.text,
        )
