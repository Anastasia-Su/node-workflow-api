from fastapi import status
from tests.setup_test_db import client, test_db


def test_create_or_update_with_assigned_parent_node_forbidden(
    client,
):
    """Message node can have only one child. So you can't specify id for already taken parent node"""

    node_id = 12
    new_node_data = {
        "message": "end",
        "parent_node_id": 7,
        "workflow_id": 1,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_for_different_workflow_forbidden(client):
    """Parent node id should exist in specified workflow"""

    node_id = 12

    new_node_data = {
        "message": "end",
        "parent_node_id": 7,
        "workflow_id": 2,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_parent_id_forbidden(
    client,
):
    """Parent node should exist in db"""

    node_id = 12

    new_node_data = {
        "message": "end",
        "parent_node_id": 100,
        "workflow_id": 1,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_workflow_id_forbidden(
    client,
):
    """You can't reference workflow that does not exist in db"""

    node_id = 12

    new_node_data = {
        "message": "end",
        "parent_node_id": 7,
        "workflow_id": 100,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_parent_of_wrong_type_forbidden(
    client,
):
    """End or Start node can't be a parent for condition node"""

    node_id = 12

    new_node_data = {
        "message": "end",
        "parent_node_id": 22,
        "workflow_id": 1,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN

    new_node_data["parent_node_id"] = 23

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN

    new_node_data["parent_node_id"] = 11

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""
    node_id = 100
    new_node_data = {
        "message": "end",
        "parent_node_id": 20,
        "workflow_id": 1,
    }

    response_retrieve = client.get(f"/end_nodes/{node_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/end_nodes/{node_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_create_or_update_with_null_parent_allowed(client):
    """You should be able to set null parent_node_id, so that you can assign it in future"""

    node_id = 19
    new_node_data = {
        "message": "end",
        "parent_node_id": 0,
        "workflow_id": 0,
    }

    response_create = client.post("/end_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_200_OK

    response_update = client.put(f"/end_nodes/{node_id}", json=new_node_data)
    assert response_update.status_code == status.HTTP_200_OK


def test_read_nodes_allowed(client):
    """You should be able to get all condition nodes"""
    response = client.get(f"/end_nodes/")

    assert response.status_code == status.HTTP_200_OK


def test_read_single_node_allowed(client):
    """You should be able to get a single condition node"""

    node_id = 12
    response = client.get(f"/end_nodes/{node_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_delete_node_allowed(client):
    """You should be able to delete a single condition node"""

    node_id = 19

    response_update = client.delete(f"/end_nodes/{node_id}")
    assert response_update.status_code == status.HTTP_200_OK
