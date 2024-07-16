from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from zoneinfo import ZoneInfo

from authentication.database import get_session
from authentication.models import User
from authentication.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

T_token = Annotated[str, Depends(oauth2_scheme)]

settings = Settings()



def get_current_user(jwt_token: T_token, session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        # Decodifica o token JWT e pega o sub (subject) que é o username
        payload = decode_access_token(jwt_token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except jwt.exceptions.ExpiredSignatureError:
        raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    # Busca o usuário no banco de dados e retorna caso exista
    user = session.scalar(select(User).filter(User.username == username))
    if user is None:
        raise credentials_exception
    return user


def decode_access_token(token: str):
    return jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
