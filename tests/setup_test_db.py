import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from database.load_mock_data import insert_mock_data, truncate_tables
from src.nodes import models

from database.dependencies import get_db
from main import app


def setup_db(engine, db):
    print("Setting up the db...")
    models.Base.metadata.create_all(bind=engine)
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "mock_db_for_tests_.json")
    insert_mock_data(db, file_path)
    db.commit()


@pytest.fixture(scope="module")
def test_db():
    # SQLALCHEMY_DATABASE_URL = "sqlite:///./testing.db"
    SQLALCHEMY_DATABASE_URL = f"{os.environ.get('MARIADB_TESTING_URL')}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    if not database_exists(engine.url):
        create_database(engine.url)

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    db = TestingSessionLocal()

    truncate_tables(db)
    setup_db(engine, db)

    yield db

    engine.dispose()


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
