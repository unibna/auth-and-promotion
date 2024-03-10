from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from loguru import logger
from starlette import status
from time import time
from typing import Optional

from app.auth import configs, schemas, services
from app.common.cache import cache
from app.common.security.crypter import crypter
from app.user.schemas import UserResponse



async def generate_session(user: UserResponse) -> Optional[schemas.Session]:
    """
    Parameters:
    - user: user.schemas.UserResponse
    Return:
    - session_id: str
        session ID
    """
    data_to_hash = (
        user.username,
        user.email,
        user.phone,
        f"{int(time())}",
    )
    plaintext = ".".join(data_to_hash)
    session_id = crypter.hash(plaintext)
    expired_datetime = datetime.now() + timedelta(days=7)
    session_data = {
        "user_id": user.id,
        "expired_at": expired_datetime.strftime("%Y-%m-%d %H:%M:%S")
    }
    cache.set(key=session_id, value=session_data, timeout=configs.SESSION_TIMEOUT)
    logger.debug(f"generate session. user: {user.id}. session_id: {session_id}")
    session = schemas.Session.parse_obj({
        "id": session_id,
        "data": session_data
    })
    return session


async def verify_session(request: Request) -> Optional[schemas.Session]:
    session_id = request.cookies.get("session_id")
    try:
        session_data = cache.get(session_id)
        if session_data:
            return schemas.Session.parse_obj({
                "id": session_id,
                "data": session_data,
            })
        else:
            raise HTTPException(
            detail="unauthorized",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        logger.error(f"failed to load session from cache. error: {e}")
        raise HTTPException(
            detail="unauthorized",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
