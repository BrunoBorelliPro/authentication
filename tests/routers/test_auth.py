from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time

from authentication.auth import create_access_token


def test_login(client, user):
    response = client.post(
        '/login', data={'username': user.username, 'password': user.password}
    )
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()


def test_login_username_incorrect(client, user):
    response = client.post(
        '/login',
        data={
            'username': f'test_user{user.username}',
            'password': user.password,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_password_incorrect(client, user):
    response = client.post(
        '/login', data={'username': user.username, 'password': 'password'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_unknown(client):
    response = client.post(
        '/login', data={'username': 'unknown', 'password': 'password'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_read_foo_bar(client, user):
    token = client.post(
        '/login', data={'username': user.username, 'password': user.password}
    ).json()['access_token']
    response = client.get(
        '/foo-bar', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_read_foo_bar_unauthorized(client):
    response = client.get('/foo-bar')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_read_foo_bar_invalid_token(client):
    token = 'invalid'
    response = client.get(
        '/foo-bar', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_foo_bar_expired_token(client, user):
    with freeze_time(datetime.now()):
        token = client.post(
            '/login',
            data={'username': user.username, 'password': user.password},
        ).json()['access_token']
    with freeze_time(datetime.now() + timedelta(minutes=31)):
        response = client.get(
            '/foo-bar', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_foo_bar_no_username(client):
    token = create_access_token(data={})
    response = client.get(
        '/foo-bar', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_read_foo_bar_unknown_user(client):
    token = create_access_token(data={'sub': 'unknown'})
    response = client.get(
        '/foo-bar', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
