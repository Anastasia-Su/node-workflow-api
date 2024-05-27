from fastapi import status
from tests.setup_test_db import client, test_db


def test_create_or_update_with_nonexistent_condition_id_forbidden(
    client,
):
    """Condition node should exist in db"""

    edge_id = 1

    new_edge_data = {"edge": "yes", "condition_node_id": 100}

    response_create = client.post("/condition_edges/", json=new_edge_data)
    assert response_create.status_code == status.HTTP_403_FORBIDDEN

    response_update = client.put(
        f"/condition_edges/{edge_id}", json=new_edge_data
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Node id should exist in db"""
    edge_id = 100
    new_edge_data = {"edge": "yes", "condition_node_id": 0}

    response_retrieve = client.get(f"/condition_edges/{edge_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(
        f"/condition_edges/{edge_id}", json=new_edge_data
    )
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/condition_edges/{edge_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_create_or_update_with_null_condition_allowed(client):
    """You should be able to set null condition_node_id, so that you can assign it in future"""

    edge_id = 9
    new_edge_data = {"edge": "yes", "condition_node_id": 0}

    response_create = client.post("/condition_edges/", json=new_edge_data)
    assert response_create.status_code == status.HTTP_200_OK

    response_update = client.put(
        f"/condition_edges/{edge_id}", json=new_edge_data
    )
    assert response_update.status_code == status.HTTP_200_OK


def test_read_edges_allowed(client):
    """You should be able to get all edges"""
    response = client.get(f"/condition_edges/")

    assert response.status_code == status.HTTP_200_OK


def test_read_single_edge_allowed(client):
    """You should be able to get a single edge"""

    edge_id = 8
    response = client.get(f"/condition_edges/{edge_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_delete_edge_allowed(client):
    """You should be able to delete a single edge"""

    edge_id = 9

    response = client.delete(f"/condition_edges/{edge_id}")
    assert response.status_code == status.HTTP_200_OK
