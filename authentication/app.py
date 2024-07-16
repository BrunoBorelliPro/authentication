from http import HTTPStatus

from fastapi import FastAPI, Response

from authentication.routers.auth import auth_router
from authentication.routers.user import user_router
from authentication.types import T_current_user

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


# T_current_user = Annotated[User, Depends(get_current_user)]
# get_current_user é uma função que retorna o usuário do token JWT
# get_current_user é uma dependência que é injetada em rotas que precisam de um usuário autenticado
@app.get('/foo-bar')
def read_foo_bar(user: T_current_user):
    return Response(status_code=HTTPStatus.NO_CONTENT)
