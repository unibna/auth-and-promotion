import os 
import sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(BASE_DIR).replace('app', '')
sys.path.append(APP_DIR)

from fastapi import FastAPI
import uvicorn

from app.common.bootstrap import init
from app.user.configs import (
    SERVICE_NAME, 
    API_SERVER_INFO,
    GRPC_SERVER_INFO,
)
from app.user.apis import router
from app.user.grpcs import start_server, stop_server


app = FastAPI()
app.include_router(
    router,
    prefix=API_SERVER_INFO.get('prefix'),
)
init(app, service_name=SERVICE_NAME)


@app.on_event("startup")
async def start_grpc_server():
    await start_server()


@app.on_event("shutdown")
async def start_grpc_server():
    await stop_server()


if __name__ == '__main__':
    uvicorn.run("main:app", 
                host=API_SERVER_INFO.get('host'), 
                port=API_SERVER_INFO.get('port'), 
                reload=True, 
                log_level="debug", 
            )
