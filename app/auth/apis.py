from fastapi import (
    APIRouter,
    HTTPException,
    Security,
    Request,
    Response,
)
import json
from loguru import logger
from starlette import status
from typing import Any

from app.auth import schemas, services
from app.auth.helpers import generate_session, verify_session
from app.user.schemas import UserResponse


router = APIRouter()


@router.post(
    path="/register",
)
async def register(
    input_: schemas.Register
) -> None:
    try:
        await services.register_user(input_)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"failed to register a new user. error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='invalid parameters'
        )


@router.post(
    path="/login/manual",
)
async def login_manual(
    input_: schemas.Login
) -> None:
    user_as_dict = await services.login_user(input_)
    session = await generate_session(UserResponse.parse_obj(user_as_dict))
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.set_cookie(key="session_id", value=session.id)
    return response


@router.post(
    path="/login/auto",
)
async def login_auto(
    request: Request,
    session: schemas.Session = Security(
        verify_session,
    )
) -> Any:
    return session
