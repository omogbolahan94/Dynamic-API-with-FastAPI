from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models, utils
from alembic import command


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_db_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user_exist(session):
    """
    Create a test user directly in the test database session. 
    This is used to verify login test
    """
    user = models.Users(
        email="gbolahan@gmail.com",
        password=utils.hash("password123")  
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"id": user.id, "email": user.email, "password": "password123"}


@pytest.fixture
def test_user_exist_not(client):
    user_data = {"email": "ola@gmail.com",
                 "password": "123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_posts(test_user_exist, session, test_user_exist_not):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user_exist['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user_exist['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user_exist['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user_exist2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts