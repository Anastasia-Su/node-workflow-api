from nodes.models import MessageStatuses
from tests.setup_test_db import client, test_db


def test_create_or_update_with_assigned_parent_node_forbidden(
    client,
):
    """Message and Start nodes can have only one child. So you can't specify id for already taken parent node"""

    node_id = 4
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 1,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_for_different_workflow_forbidden(client):
    """Parent node id should exist in specified workflow"""

    node_id = 3

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 22,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_with_nonexistent_parent_id_forbidden(
    client,
):
    """Parent node should exist in db"""

    node_id = 4

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 100,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_with_nonexistent_workflow_id_forbidden(
    client,
):
    """You can't reference workflow that does not exist in db"""

    node_id = 4

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 100,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 403


def test_create_or_update_with_parent_of_wrong_type_forbidden(
    client,
):
    """End node can't be a parent for any node"""

    node_id = 3

    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 11,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 403

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 403


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""

    node_id = 100
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    response_retrieve = client.get(f"/message_nodes/{node_id}/")
    assert response_retrieve.status_code == 404

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 404

    response_delete = client.delete(f"/message_nodes/{node_id}")
    assert response_delete.status_code == 404


def test_create_or_update_with_null_parent_allowed(client):
    """You should be able to set null parent_node_id, so that you can assign it in future"""

    node_id = 4
    new_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 0,
        "parent_condition_edge_id": 0,
        "workflow_id": 2,
    }

    response_create = client.post("/message_nodes/", json=new_node_data)
    assert response_create.status_code == 200

    response_update = client.put(
        f"/message_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == 200


def test_read_message_nodes_allowed(client):
    """You should be able to retrieve list of all message_nodes"""

    response = client.get(f"/message_nodes/")

    assert response.status_code == 200


def test_read_single_node_allowed(client):
    """You should be able retrieve a single message_node"""

    node_id = 3
    response = client.get(f"/message_nodes/{node_id}/")

    assert response.status_code == 200


def test_delete_node_allowed(client):
    """You should be able to delete message_node"""

    node_id = 4

    response_update = client.delete(f"/message_nodes/{node_id}")
    assert response_update.status_code == 200
