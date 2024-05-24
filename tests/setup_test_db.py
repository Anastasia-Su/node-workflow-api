import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load_mock_data import insert_mock_data
from nodes import models

from dependencies import get_db
from main import app


# def setup_db(engine, db):
#     models.Base.metadata.create_all(bind=engine)
#     insert_mock_data(db, "mock_db.json")
# setup_test_db(db)


# Function to teardown the test database
# def teardown_test_db(engine):
#     models.Base.metadata.drop_all(bind=engine)
#     current_dir = os.path.dirname(__file__)
#     file_path = os.path.join(current_dir, "test.db")
#     if os.path.exists(file_path):
#         os.remove(file_path)


#
# # Pytest fixture to setup and teardown the test database
# @pytest.fixture(scope="module")
# def test_db():
#     SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
#     TestingSessionLocal = sessionmaker(
#         autocommit=False, autoflush=False, bind=engine
#     )
#
#     db = TestingSessionLocal()
#
#     models.Base.metadata.create_all(bind=engine)
#     insert_mock_data(db, "mock_db.json")
#
#     # setup_db(engine, db)
#
#     yield db
#     teardown_test_db(engine)


@pytest.fixture(scope="module")
def test_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Uncomment below string to load mock data to test db.
    # Before run tests again, comment it.
    # insert_mock_data(db, "mock_db.json")
    yield db
    db.close()


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
