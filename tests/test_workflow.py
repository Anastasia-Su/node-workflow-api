from urllib import response

from fastapi import status
from tests.setup_test_db import client, test_db


def test_read_update_delete_with_nonexistent_id_forbidden(
    client,
):
    """Workflow id should exist in db"""
    workflow_id = 100
    new_node_data = {
        "name": "W1",
    }

    response_retrieve = client.get(f"/workflows/{workflow_id}/")
    assert response_retrieve.status_code == status.HTTP_404_NOT_FOUND

    response_update = client.put(
        f"/workflows/{workflow_id}", json=new_node_data
    )
    assert response_update.status_code == status.HTTP_404_NOT_FOUND

    response_delete = client.delete(f"/workflows/{workflow_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND


def test_read_workflows_allowed(client):
    """You should be able to get all workflows"""
    response = client.get(f"/workflows/")

    assert response.status_code == status.HTTP_200_OK


def test_read_single_workflow_allowed(client):
    """You should be able to get a single workflow"""

    workflow_id = 1
    response = client.get(f"/workflows/{workflow_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_workflow_executed(client):
    """You should be able to execute a workflow"""

    workflow_id = 1

    response = client.post(
        f"/workflows/execute/{workflow_id}?draw_graph=false"
    )
    assert response.status_code == status.HTTP_200_OK
    assert "graph" in response.json()


def test_delete_workflow_allowed(client):
    """You should be able to delete a single workflow"""

    workflow_id = 4

    response = client.delete(f"/workflows/{workflow_id}")
    assert response.status_code == status.HTTP_200_OK
