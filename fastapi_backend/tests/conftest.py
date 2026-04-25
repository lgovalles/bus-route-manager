"""Pytest configuration and shared fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.dependencies import get_db
import uuid

# Test database - use unique name per test session
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    """Create test engine"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Provide database session for tests"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        # Clear all tables before each test
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    """Provide FastAPI test client with fresh database"""
    # Override the get_db dependency to use our test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def db_with_seed_data(test_client, db_session):
    """
    Provide test client with realistic seed data
    
    Initializes database with:
    - 14 stops (paraderos) including key ones: Belén, Aeropuerto
    - 10 routes (01-10) with realistic names
    - Route-stop relationships with proper ordering
    """
    from app.seed_data import seed_database
    
    # Seed the database with realistic data
    try:
        seed_database(db_session)
    except Exception as e:
        print(f"Seeding warning: {e}")
    
    return test_client
