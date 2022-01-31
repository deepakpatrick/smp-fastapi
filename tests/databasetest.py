from operator import contains
from fastapi.testclient import TestClient
from app.main import app

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
    