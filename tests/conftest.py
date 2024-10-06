from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import pytest
from alembic import command

client = TestClient(app)

#SQlALCHEMY_DATABASE_URL = 'postgresql://postgres:anuj2006@localhost:5432/fastapi_test'
SQlALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@'
                           f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')

engine = create_engine(SQlALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



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
    user_data = {"email":"dhoni1@gmail.com","password":"5cups"}
    response = client.post("/users/",json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user