from fastapi import status
from tests.setup_test_db import client, test_db


def test_create_or_update_with_assigned_parent_node_forbidden(
    client,
):
    """Message node can have only one child.
    So you can't specify id for already taken parent node"""

    node_id = 8
    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": 5,
        "parent_message_node_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_assigned_parent_condition_node_forbidden(
    client,
):
    """Condition node can have only two children.
    So you can't specify id for already taken parent node"""

    node_id = 8
    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": 9,
        "parent_message_node_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_for_different_workflow_forbidden(client):
    """Parent node id should exist in specified workflow"""

    node_id = 8

    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": 20,
        "parent_message_node_id": None,
        "workflow_id": 2,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_parent_id_forbidden(
    client,
):
    """Parent node should exist in db"""

    node_id = 8

    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": 100,
        "parent_message_node_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_parent_message_id_forbidden(
    client,
):
    """Parent message node should exist in db"""

    node_id = 8

    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": None,
        "parent_message_node_id": 100,
        "workflow_id": 1,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_nonexistent_workflow_id_forbidden(
    client,
):
    """You can't reference workflow that does not exist in db"""

    node_id = 8

    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": None,
        "parent_message_node_id": None,
        "workflow_id": 100,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_create_or_update_with_parent_of_wrong_type_forbidden(
    client,
):
    """End or Start node can't be a parent for condition node"""

    node_id = 8

    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": 22,
        "parent_message_node_id": None,
        "workflow_id": 1,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN

    new_node_data["parent_node_id"] = 12

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""
    node_id = 100
    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": None,
        "parent_message_node_id": None,
        "workflow_id": 1,
    }

    response_retrieve = client.get(f"/condition_nodes/{node_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/condition_nodes/{node_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_create_or_update_with_null_parent_allowed(client):
    """You should be able to set null parent_node_id,
    so that you can assign it in future"""

    node_id = 21
    new_node_data = {
        "condition": "status == sent",
        "parent_node_id": None,
        "parent_message_node_id": None,
        "workflow_id": 2,
    }

    response_create = client.post("/condition_nodes/", json=new_node_data)
    assert response_create.status_code == status.HTTP_200_OK

    response_update = client.put(
        f"/condition_nodes/{node_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_200_OK

    assert response_create.json()["condition"] == new_node_data["condition"]
    assert (
        response_create.json()["workflow_id"] == new_node_data["workflow_id"]
    )

    assert response_update.json()["condition"] == new_node_data["condition"]
    assert (
        response_update.json()["workflow_id"] == new_node_data["workflow_id"]
    )


def test_read_nodes_allowed(client):
    """You should be able to get all condition nodes"""

    response = client.get("/condition_nodes/")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        "/condition_nodes/?condition=sent&parent_message_node_id=3"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_read_single_node_allowed(client):
    """You should be able to get a single condition node"""

    node_id = 8
    response = client.get(f"/condition_nodes/{node_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_delete_node_allowed(client):
    """You should be able to delete a single condition node"""

    node_id = 21

    response = client.delete(f"/condition_nodes/{node_id}")
    assert response.status_code == status.HTTP_200_OK
