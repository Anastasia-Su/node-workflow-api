import json
import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load_mock_data import insert_mock_data
from nodes import models

from dependencies import get_db
from main import app
from nodes.models import MessageStatuses, NodeTypes
from tests.setup_test_db import setup_test_db


def setup_db(engine, db):
    models.Base.metadata.create_all(bind=engine)
    insert_mock_data(db, "mock_db.json")
    # setup_test_db(db)


# Function to teardown the test database
def teardown_test_db(engine):
    models.Base.metadata.drop_all(bind=engine)
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "test.db")
    if os.path.exists(file_path):
        os.remove(file_path)


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


# Use the TestClient to send requests to the application
@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


def test_create_or_update_message_node_allowed(client):
    node_id = 4

    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 2,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post(
        "/message_nodes/", json=new_message_node_data
    )
    assert response_create.status_code == 200

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 200


def test_create_or_update_with_assigned_parent_node_forbidden(
    client,
):
    """Message and Start nodes can have only one child. So you can't specify id for already taken parent node"""

    node_id = 4
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response_create = client.post(
        "/message_nodes/", json=new_message_node_data
    )
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_for_different_workflow_forbidden(client):
    node_id = 3

    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post(
        "/message_nodes/", json=new_message_node_data
    )
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_with_nonexistent_parent_id_forbidden(
    client,
):
    node_id = 4

    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 100,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post(
        "/message_nodes/", json=new_message_node_data
    )
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_with_null_parent_allowed(client):

    node_id = 4
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post(
        "/message_nodes/", json=new_message_node_data
    )
    assert response_create.status_code == 200

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 200


def test_read_message_nodes_allowed(client):
    response = client.get(f"/message_nodes/")

    assert response.status_code == 200


def test_read_single_message_node_allowed(client):
    node_id = 3
    response = client.get(f"/message_nodes/{node_id}/")

    assert response.status_code == 200


def test_read_or_update_with_nonexistent_id_forbidden(
    client,
):
    node_id = 100
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response_retrieve = client.get(f"/message_nodes/{node_id}/")
    assert response_retrieve.status_code == 404

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_message_node_data
    )
    assert response_update.status_code == 404
