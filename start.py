import re
from os.path import dirname, isfile, join

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import files
import levels
import proxy
from dependencies import authenticate

app = FastAPI(dependencies=[Depends(authenticate)])
app.include_router(files.router)
app.include_router(levels.router)
app.include_router(proxy.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    version = None
    if isfile(join(dirname(__file__), "pyproject.toml")):
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            text = f.read()
            version = re.search(r"version\s?=\s?\"(.+?)\"", text).group(1)
    return {"version": version}


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        {"detail": type(exc).__name__ + ": " + str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=23287)
    exit()
