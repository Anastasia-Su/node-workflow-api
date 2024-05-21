import json
import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.mock_models import Base, Node
from dependencies import get_db
from main import app
from nodes.models import MessageStatuses, NodeTypes

# from tests.load_mock_data_for_tests import load_mock_data, insert_mock_data
from tests.setup_test_db import setup_test_db


db = setup_test_db()
# node_start = Node(
#     id=1,
#     node_type=NodeTypes.START,
# )
# node_start2 = Node(
#     id=2,
#     node_type=NodeTypes.START,
# )
#
# node_message = Node(
#     id=3,
#     node_type=NodeTypes.MESSAGE,
# )
# node_message2 = Node(
#     id=4,
#     node_type=NodeTypes.MESSAGE,
# )
#
# db.add(node_start)
# db.add(node_start2)
# db.add(node_message)
# db.add(node_message2)
# db.commit()


def override_get_db():
    try:
        yield db
    finally:
        db.remove()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_message_node_allowed():
    new_message_node_data = {
        "status": MessageStatuses.PENDING,
        "text": "Test message node",
        "parent_node_id": 2,
        # "parent_condition_edge_id": 0,
        "workflow_id": 1,
    }

    # db.query(models.MessageNode).get.return_value = mock_data_existing

    response = client.post("/message_nodes/", json=new_message_node_data)
    # assert response.status_code == 200
    assert response.json()["detail"] == "hhllllll"


#
# def test_create_message_node_with_assigned_parent_start_node_forbidden(
#     override_get_db,
# ):
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node",
#         "parent_node_id": 1,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 1,
#     }
#
#     response = client.post("/message_nodes/", json=new_message_node_data)
#     assert response.status_code == 403
#
#
# def test_create_message_node_for_different_workflow_forbidden(mock_db_session):
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node",
#         "parent_node_id": 1,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 2,
#     }
#
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.post("/message_nodes/", json=new_message_node_data)
#     assert response.status_code == 403
#
#
# def test_create_message_node_with_nonexistent_parent_id_forbidden(
#     override_get_db,
# ):
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node",
#         "parent_node_id": 10,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 2,
#     }
#     mock_db_session.query(models.Node).get.return_value = None
#
#     response = client.post("/message_nodes/", json=new_message_node_data)
#     assert response.status_code == 403
#
#
# def test_create_message_node_with_null_parent_allowed(mock_db_session):
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node",
#         "parent_node_id": 0,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 2,
#     }
#
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.post("/message_nodes/", json=new_message_node_data)
#     assert response.status_code == 200
#


# data = load_mock_data("mock_db.json")
# insert_mock_data(db, data)
# db.commit()


# Override the get_db dependency in your app
# def override_get_db():
#     try:
#         yield db
#     finally:
#         db.remove()
#
#
# app.dependency_overrides[get_db] = override_get_db
#
# # Create a TestClient
# client = TestClient(app)


#
# def test_read_message_nodes_allowed(mock_db_session):
#     response = client.get(f"/message_nodes/")
#
#     assert response.status_code == 200
#
#
# def test_read_single_message_node_with_nonexistent_id_forbidden(
#     override_get_db,
# ):
#     node_id = 9
#     mock_db_session.query(models.MessageNode).get.return_value = None
#     response = client.get(f"/message_nodes/{node_id}/")
#
#     assert response.status_code == 404
#
#
# def test_read_single_message_node_allowed(mock_db_session):
#     node_id = 3
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.get(f"/message_nodes/{node_id}/")
#
#     assert response.status_code == 200
#
#
# #
# # def test_update_message_node_with_assigned_parent_start_node_forbidden(
# #     override_dependency
# # ):
# #     node_id = 3
# #
# #     new_message_node_data = {
# #         "status": MessageStatuses.PENDING,
# #         "text": "Test message node updated",
# #         "parent_node_id": 1,
# #         "parent_condition_edge_id": 0,
# #         "workflow_id": 1,
# #     }
# #
# #     mock_db_session.query(models.MessageNode).get.return_value = (
# #         mock_data_existing2
# #     )
# #
# #     response = client.put(
# #         f"/message_nodes/{node_id}", json=new_message_node_data
# #     )
# #     assert response.status_code == 403
# #     # assert response.json()["detail"] == "hhllllll"
#
#
# def test_update_message_node_for_different_workflow_forbidden(mock_db_session):
#     node_id = 3
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node",
#         "parent_node_id": 1,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 2,
#     }
#
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.put(
#         f"/message_nodes/{node_id}", json=new_message_node_data
#     )
#     assert response.status_code == 403
#
#
# def test_update_message_node_with_nonexistent_parent_id_forbidden(
#     override_get_db,
# ):
#     node_id = 3
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node update",
#         "parent_node_id": 11,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 1,
#     }
#     #
#     # mock_db_session.query(models.MessageNode).get.return_value = (
#     #     mock_data_existing
#     # )
#     mock_db_session.query(models.Node).get.return_value = None
#
#     response = client.put(
#         f"/message_nodes/{node_id}", json=new_message_node_data
#     )
#     assert response.status_code == 403
#     assert response.json()["detail"] == "hhllllll"
#
#
# def test_update_message_node_with_null_parent_allowed(mock_db_session):
#     node_id = 3
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node update",
#         "parent_node_id": 0,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 1,
#     }
#     #
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.put(
#         f"/message_nodes/{node_id}", json=new_message_node_data
#     )
#     assert response.status_code == 200
#
#     updated_message_node = response.json()
#     assert updated_message_node["status"] == new_message_node_data["status"]
#     assert updated_message_node["text"] == new_message_node_data["text"]
#     assert (
#         updated_message_node["parent_node_id"]
#         == new_message_node_data["parent_node_id"]
#     )
#     assert (
#         updated_message_node["parent_condition_edge_id"]
#         == new_message_node_data["parent_condition_edge_id"]
#     )
#     assert (
#         updated_message_node["workflow_id"]
#         == new_message_node_data["workflow_id"]
#     )
#
#
# def test_update_message_node_allowed(mock_db_session):
#     node_id = 3
#
#     new_message_node_data = {
#         "status": MessageStatuses.PENDING,
#         "text": "Test message node updated",
#         "parent_node_id": 1,
#         "parent_condition_edge_id": 0,
#         "workflow_id": 1,
#     }
#     mock_db_session.query(models.MessageNode).get.return_value = (
#         mock_data_existing
#     )
#
#     response = client.put(
#         f"/message_nodes/{node_id}", json=new_message_node_data
#     )
#
#     assert response.status_code == 200
#
#     updated_message_node = response.json()
#     assert updated_message_node["status"] == new_message_node_data["status"]
#     assert updated_message_node["text"] == new_message_node_data["text"]
#     assert (
#         updated_message_node["parent_node_id"]
#         == new_message_node_data["parent_node_id"]
#     )
#     assert (
#         updated_message_node["parent_condition_edge_id"]
#         == new_message_node_data["parent_condition_edge_id"]
#     )
#     assert (
#         updated_message_node["workflow_id"]
#         == new_message_node_data["workflow_id"]
#     )
