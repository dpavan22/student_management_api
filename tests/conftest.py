from sqlalchemy import create_engine , StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from pytest import fixture
from app.database import Base
from app.main import app
from app.dependencies import get_db


test_engine = create_engine(url="sqlite:///:memory:",
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind=test_engine)

@fixture
def test_db():
    
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.create_all(bind=test_engine)

    
@fixture
def client(test_db):
    def override_get_db():
        yield test_db
        app.dependency_overrides[get_db] = override_get_db
        
        yield TestClient
        
        app.dependency_overrides.clear()



    
