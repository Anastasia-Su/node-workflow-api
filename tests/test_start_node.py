from fastapi import status
from tests.setup_test_db import client, test_db


def test_create_or_update_more_than_one_node_in_workflow_forbidden(client):
    """Workflow can have only one start node"""

    node_id = 1

    new_node_data = {
        "message": "start",
        "workflow_id": 2,
    }

    response_create = client.post("/start_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/start_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""
    node_id = 100
    new_node_data = {
        "message": "start",
        "workflow_id": 2,
    }

    response_retrieve = client.get(f"/start_nodes/{node_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(f"/start_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/start_nodes/{node_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_read_nodes_allowed(client):
    """You should be able to get all start nodes"""
    response = client.get(f"/start_nodes/")

    assert response.status_code == status.HTTP_200_OK


def test_read_single_node_allowed(client):
    """You should be able to get a single start node"""

    node_id = 1
    response = client.get(f"/start_nodes/{node_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_delete_node_allowed(client):
    """You should be able to delete a single start node"""

    node_id = 13

    response = client.delete(f"/start_nodes/{node_id}")
    assert response.status_code == status.HTTP_200_OK


def test_create_or_update_with_nonexistent_workflow_id_forbidden(
    client,
):
    """You can't reference workflow that does not exist in db"""

    node_id = 1

    new_node_data = {
        "message": "start",
        "workflow_id": 100,
    }

    response_create = client.post("/start_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/start_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_400_BAD_REQUEST,
    ]
