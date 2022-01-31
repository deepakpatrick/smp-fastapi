from operator import contains
from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import create_access_token
from app import models

from app.database import Base, get_db, sessionmaker, create_engine, settings
import pytest
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:deepak@localhost:5432/fastapi-test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# client = TestClient(app)

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
def test_user(client):
    user_data = {"email": "he214@g.com",
    "password":"vvv"}
    response = client.post("/users/",json=user_data)
    assert response.status_code == 201
    print(response.json())
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "she214@g.com",
    "password":"sss"}
    response = client.post("/users/",json=user_data)
    assert response.status_code == 201
    print(response.json())
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token( token_pay_load = {"user_id":test_user['id']} )
    

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def sample_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title"   : "post 1",
            "contents" : "some contents 1",
            "owner_id" : test_user['id']
        },
        {
            "title"   : "post 2",
            "contents" : "some contents 2",
            "owner_id" : test_user['id']
        },
        {
            "title"   : "post 3",
            "contents" : "some contents 3",
            "owner_id" : test_user['id']
        },
        {
            "title"   : "post from testuser2",
            "contents" : "some contents from testuser2",
            "owner_id" : test_user2['id']
        }       
    ]
    
    def create_post_models(post):
        return models.SocialMediaPosts(**post)
    
    postmap = map(create_post_models, posts_data)
    posts = list(postmap)    
    session.add_all(posts)
    session.commit()
    posts = session.query(models.SocialMediaPosts).all()
    return posts