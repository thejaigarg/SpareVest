# Test configuration
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import TEST_DATABASE_URL
from app.core.database import Base, get_db
from fastapi.testclient import TestClient
from app.main import app

print(TEST_DATABASE_URL)
# Cloud test DB engine
engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# (Optional but recommended) Create schema at start of test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Drop all tables, then create (VERY safe for test-only DB)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Optionally, drop all at end too (clean up)
    Base.metadata.drop_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    yield TestClient(app)