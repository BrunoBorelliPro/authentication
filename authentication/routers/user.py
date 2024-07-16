from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select

from authentication.models import User
from authentication.schemas import UserListSchema, UserPublicSchema, UserSchema
from authentication.types import T_current_user, T_Session

user_router = APIRouter(
    tags=['users'],
)


@user_router.post(
    '/users', response_model=UserPublicSchema, status_code=HTTPStatus.CREATED
)
def create_user(user: UserSchema, session: T_Session):
    userDB = session.scalar(
        select(User).filter(User.username == user.username)
    )
    if userDB:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already exists',
        )

    session.add(User(username=user.username, password=user.password))
    session.commit()
    userDB = session.scalar(
        select(User).filter(User.username == user.username)
    )

    return userDB


@user_router.get('/users', response_model=UserListSchema)
def read_users(session: T_Session):
    users = session.execute(select(User)).scalars().all()
    return {'users': users}


@user_router.get('/users/{user_id}', response_model=UserPublicSchema)
def read_user(user_id: int, session: T_Session):
    user = session.scalar(select(User).filter(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    return user


@user_router.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: T_Session, user: T_current_user):
    if user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='User can only delete itself',
        )
    session.delete(user)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)


@user_router.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(
    user_id: int,
    user_form: UserSchema,
    session: T_Session,
    current_user: T_current_user,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='User can only update itself',
        )

    current_user.username = user_form.username
    current_user.password = user_form.password
    session.commit()
    session.refresh(current_user)
    return current_user
