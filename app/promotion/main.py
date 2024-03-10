import os 
import sys
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(BASE_DIR).replace('app', '')
sys.path.append(APP_DIR)

from fastapi import FastAPI
import uvicorn

from app.common.bootstrap import init
from app.promotion.configs import SERVICE_NAME, API_SERVER_INFO
from app.promotion.apis.campaigns import router


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