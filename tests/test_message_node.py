from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from dependencies import get_db
from main import app
from nodes import models
from nodes.models import MessageStatuses, NodeTypes


mock_data_start = models.StartNode(
    id=1,
    message="Starting",
    workflow_id=1,
    node_type=NodeTypes.START,
)

mock_data_existing = models.MessageNode(
    id=2,
    status=MessageStatuses.PENDING,
    text="Existing message node",
    parent_node_id=1,
    parent_condition_edge_id=0,
    workflow_id=1,
)

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.query(models.Node).get.return_value = mock_data_start
    # session.query(
    #     models.MessageNode
    # ).filter.return_value.first.return_value = mock_data_existing
    session.query(models.MessageNode).all.return_value = [mock_data_existing]

    return session


@pytest.fixture
def override_get_db(mock_db_session):
    app.dependency_overrides[get_db] = lambda: mock_db_session
    yield
    app.dependency_overrides.pop(get_db)


client = TestClient(app)


def test_create_message_node_with_assigned_parent_start_node_forbidden(
    override_get_db, mock_db_session
):
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response = client.post("/message_nodes/", json=new_message_node_data)
    assert response.status_code == 403


def test_create_message_node_for_different_workflow_forbidden(
    override_get_db, mock_db_session
):
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response = client.post("/message_nodes/", json=new_message_node_data)
    assert response.status_code == 403


def test_create_message_node_with_nonexistent_parent_id_forbidden(
    override_get_db, mock_db_session
):
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 10,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }
    mock_db_session.query(models.Node).get.return_value = None

    response = client.post("/message_nodes/", json=new_message_node_data)
    assert response.status_code == 403


def test_create_message_node_with_null_parent_allowed(
    override_get_db, mock_db_session
):
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response = client.post("/message_nodes/", json=new_message_node_data)
    assert response.status_code == 200


def test_create_message_node_allowed(override_get_db, mock_db_session):
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 2,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response = client.post("/message_nodes/", json=new_message_node_data)
    assert response.status_code == 200


def test_read_message_nodes(override_get_db, mock_db_session):
    response = client.get(f"/message_nodes/")

    assert response.status_code == 200


def test_read_single_message_node(override_get_db, mock_db_session):
    node_id = 2
    mock_db_session.query(models.MessageNode).get.return_value = (
        mock_data_existing
    )
    response = client.get(f"/message_nodes/{node_id}/")

    assert response.status_code == 200


def test_read_single_message_node_with_nonexistent_id_forbidden(
    override_get_db, mock_db_session
):
    node_id = 9
    mock_db_session.query(models.MessageNode).get.return_value = None
    response = client.get(f"/message_nodes/{node_id}/")

    assert response.status_code == 404
