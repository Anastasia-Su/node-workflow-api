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


def test_read_single_node_allowed(client):
    """You should be able to get a single workflow"""

    workflow_id = 1
    response = client.get(f"/workflows/{workflow_id}/")

    assert response.status_code == status.HTTP_200_OK


def test_workflow_no_start_node(client):
    """Workflow should start with a Start node"""

    workflow_id = 3

    response = client.post(f"/workflows/execute/{workflow_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# def test_workflow_executed(client):
#     """You should be able to execute a workflow"""
#
#     workflow_id = 1
#
#     response = client.post(
#         f"/workflows/execute/", json={"workflow_id": workflow_id}
#     )
#     assert response.status_code == status.HTTP_200_OK

#
# def test_delete_workflow_allowed(client):
#     """You should be able to delete a single workflow"""
#
#     workflow_id = 3
#
#     response = client.delete(f"/workflows/{workflow_id}")
#     assert response.status_code == status.HTTP_200_OK
