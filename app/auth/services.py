import json
import requests

from app.auth.schemas import Login, Register
from app.common.configs import ROOT_URLS
from app.utils.utils import datetime_encoder


async def login_user(payload: Login) -> dict:
    url = ROOT_URLS.get('user') + "/login"
    payload = payload.dict()
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code in [200, 204]:
        return json.loads(response.content)
    else:
        raise Exception(f"failed to login user. error: {response.content}")


async def register_user(payload: Register) -> dict:
    url = ROOT_URLS.get('user') + "/register"
    payload = payload.dict()
    response = requests.post(url, data=json.dumps(payload, default=datetime_encoder))
    if response.status_code in [200, 204]:
        return json.loads(response.content)
    else:
        raise Exception(f"failed to register user. error: {response.content}")
