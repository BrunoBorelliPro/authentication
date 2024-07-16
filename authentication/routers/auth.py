from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from authentication.auth import create_access_token
from authentication.models import User
from authentication.types import T_form_data, T_Session

auth_router = APIRouter(
    tags=['auth'],
)


@auth_router.post('/login')
def make_login(session: T_Session, form: T_form_data):
    user = session.scalar(select(User).filter(User.username == form.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )
    if user.password != form.password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    token = create_access_token(data={'sub': form.username})

    return {'access_token': token, 'token_type': 'bearer'}
