"""Fixtures pytest."""
import os
import pytest
from fastapi.testclient import TestClient

os.environ['DATABASE_URL'] = 'sqlite:///./test_pytest.db'

from database import init_db, Base, engine
from main import app
from seed import seed_data


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    if os.path.exists('test_pytest.db'):
        os.remove('test_pytest.db')
    init_db()
    seed_data()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists('test_pytest.db'):
        os.remove('test_pytest.db')


@pytest.fixture
def client():
    return TestClient(app)
