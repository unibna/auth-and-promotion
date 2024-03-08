from fastapi import (
    APIRouter,
    HTTPException,
    Response,
    Request,
    Security,
)
from loguru import logger
from starlette import status
from typing import (
    Any,
    List,
)

from app.common.security.crypter import crypter
from app.user import models, schemas
from app.user.helpers import get_credential_types



router = APIRouter()


@router.get("/")
async def list_users() -> List[schemas.UserResponse]:
    try:
        users = await models.User.all()
        return users
    except Exception as e:
        logger.error(f"failed to list users. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@router.get("/{user_id}")
async def get_user(
    user_id: int
) -> schemas.UserResponse:
    try:
        user = await models.User.get(id=user_id)
        return user
    except Exception as e:
        logger.error(f"failed to get user. user_id: {user_id}. error: {e}")
        raise HTTPException(
            detail="internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/")
async def create_user(
    payload: schemas.UserCreate
) -> Any:  
    try:
        await models.User.create(**payload.dict())
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"failed to create a new user. error: {e}")
        raise HTTPException(
            detail="invalid parameters",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
) -> Any:  
    try:
        await models.User.get(id=user_id).update(**payload.dict())
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"failed to update user. user_id: {user_id}. error: {e}")
        raise HTTPException(
            detail="invalid parameters",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.post("/login")
async def login_user(
    payload: schemas.UserLogin
) -> schemas.UserResponse:
    credential_type = get_credential_types(account=payload.account)
    user = await models.User.filter(**credential_type).first()
    hashed_payload_password = str(crypter.hash_password(payload.password.encode()))
    if hashed_payload_password == user.password:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid account or password",
        )
    

@router.post("/register")
async def register_user(
    payload: schemas.UserRegister
) -> schemas.UserResponse:
    try:
        user = await models.User.create(**payload.dict())
        return user
    except Exception as e:
        logger.error(f"failed to create a new user. error: {e}")
        raise HTTPException(
            detail="invalid parameters",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
