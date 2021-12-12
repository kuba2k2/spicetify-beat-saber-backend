import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=23287)
    exit()
