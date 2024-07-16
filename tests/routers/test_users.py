from http import HTTPStatus

from authentication.schemas import UserPublicSchema


def test_create_user(client):
    response = client.post(
        '/users', json={'username': 'user4', 'password': 'password4'}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_create_user_duplicate(client, user):
    response = client.post(
        '/users', json={'username': user.username, 'password': 'password4'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_invalid(client):
    response = client.post('/users', json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_invalid_username(client):
    response = client.post(
        '/users', json={'username': 'us', 'password': 'aslkdhlaskhdl'}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_invalid_password(client):
    response = client.post(
        '/users', json={'username': 'user4', 'password': ''}
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_read_users(client, user):
    response = client.get('/users')
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, token, user):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_forbidden(client, token):
    response = client.delete(
        '/users/999', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'User can only delete itself'}


def test_update_user(client, token, user):
    response = client.put(
        f'/users/{user.id}',
        json={'username': 'user4', 'password': 'password4'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': user.id, 'username': 'user4'}


def test_update_user_forbidden(client, token):
    response = client.put(
        '/users/999',
        json={'username': 'user4', 'password': 'password4'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'User can only update itself'}
