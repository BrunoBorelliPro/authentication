import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from authentication.app import app
from authentication.auth import create_access_token
from authentication.database import get_session
from authentication.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    db_user = User(username='user1', password='password1')
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@pytest.fixture
def token(user):
    token = create_access_token(data={'sub': user.username})
    return token
