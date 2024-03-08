import os 
import sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(BASE_DIR).replace('app', '')
sys.path.append(APP_DIR)

from fastapi import FastAPI
import uvicorn

from app.auth.configs import *
from app.auth.apis import router
from app.common.bootstrap import init


app = FastAPI()
app.include_router(
    router,
    prefix=API_SERVER_INFO.get('prefix'),
)
init(app, SERVICE_NAME)


if __name__ == '__main__':
    uvicorn.run("main:app", 
                host=API_SERVER_INFO.get('host'), 
                port=API_SERVER_INFO.get('port'), 
                reload=True, 
                log_level="debug", 
            )