from fastapi import status
from nodes.models import MessageStatuses, MessageNode
from tests.setup_test_db import client, test_db


def test_create_or_update_with_assigned_parent_node_forbidden(
    client,
):
    """Message and Start nodes can have only one child.
    So you can't specify id for already taken parent node"""

    node_id = 4
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_assigned_parent_condition_node_forbidden(
    client,
):
    """Condition node can have only two children.
    So you can't specify id for already taken parent node"""

    node_id = 20
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 9,
        "parent_condition_edge_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_for_different_workflow_forbidden(client):
    """Parent node id should exist in specified workflow"""

    node_id = 3

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 22,
        "parent_condition_edge_id": None,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_parent_id_forbidden(
    client,
):
    """Parent node should exist in db"""

    node_id = 4

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 100,
        "parent_condition_edge_id": None,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_workflow_id_forbidden(
    client,
):
    """You can't reference workflow that does not exist in db"""

    node_id = 4

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": None,
        "parent_condition_edge_id": None,
        "workflow_id": 100,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_parent_of_wrong_type_forbidden(
    client,
):
    """End node can't be a parent for any node"""

    node_id = 3

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 11,
        "parent_condition_edge_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""

    node_id = 100
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": None,
        "parent_condition_edge_id": None,
        "workflow_id": 1,
    }

    response_retrieve = client.get(f"/message_nodes/{node_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/message_nodes/{node_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_create_or_update_with_null_parent_allowed(client):
    """You should be able to set null parent_node_id,
    so that you can assign it in future"""

    node_id = 4
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": None,
        "parent_condition_edge_id": None,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_200_OK

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_200_OK

    assert response_create.json()["status"] == new_node_data["status"]
    assert response_create.json()["text"] == new_node_data["text"]
    assert (
        response_create.json()["workflow_id"] == new_node_data["workflow_id"]
    )

    assert response_update.json()["status"] == new_node_data["status"]
    assert response_update.json()["text"] == new_node_data["text"]
    assert (
        response_update.json()["workflow_id"] == new_node_data["workflow_id"]
    )


def test_read_message_nodes_allowed(client):
    """You should be able to retrieve list of all message_nodes"""

    response = client.get("/message_nodes/")
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/message_nodes/?text=open")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 4

    response = client.get("/message_nodes/?text=sent&status=pending")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_read_single_node_allowed(client):
    """You should be able to retrieve a single message_node"""

    node_id = 3
    response = client.get(f"/message_nodes/{node_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_delete_node_allowed(client):
    """You should be able to delete message_node"""

    node_id = 4

    response = client.delete(f"/message_nodes/{node_id}")
    assert response.status_code == status.HTTP_200_OK

    response_after_delete = client.get(f"/message_nodes/{node_id}/")
    assert response_after_delete.status_code == status.HTTP_404_NOT_FOUND
