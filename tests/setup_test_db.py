import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load_mock_data import insert_mock_data
from nodes import models

from dependencies import get_db
from main import app


def setup_db(engine, db):
    models.Base.metadata.create_all(bind=engine)
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "mock_db_for_tests.json")
    insert_mock_data(db, file_path)


def teardown_test_db(engine):
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    db = TestingSessionLocal()
    teardown_test_db(engine)
    setup_db(engine, db)

    yield db


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
