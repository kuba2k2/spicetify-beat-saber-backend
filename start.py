import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import files
import levels
import proxy
from dependencies import authenticate
from settings import Settings

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

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
    exit()
