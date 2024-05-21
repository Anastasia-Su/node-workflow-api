import json
import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.mock_models import Base
from dependencies import get_db
from main import app
from nodes import models
from nodes.models import MessageStatuses, NodeTypes
from tests.load_mock_data_for_tests import load_mock_data, insert_mock_data

# from tests.mock_models import db

#
# mock_data_start_node = models.StartNode(
#     id=1,
#     node_type=NodeTypes.START,
# )
#
# mock_data_start = models.StartNode(
#     id=mock_data_start_node.id,
#     message="Starting",
#     workflow_id=1,
# )
#
#
# mock_data_start2_node = models.StartNode(
#     id=2,
#     node_type=NodeTypes.START,
# )
#
#
# mock_data_start2 = models.StartNode(
#     id=mock_data_start2_node.id,
#     message="Starting",
#     workflow_id=1,
#     node_type=NodeTypes.START,
# )
#
#
# mock_data_existing_node = models.StartNode(
#     id=3,
#     node_type=NodeTypes.MESSAGE,
# )
#
# mock_data_existing = models.MessageNode(
#     id=mock_data_existing_node.id,
#     status=MessageStatuses.PENDING,
#     text="Existing message node",
#     parent_node_id=1,
#     parent_condition_edge_id=0,
#     workflow_id=1,
# )
#
#
# mock_data_existing2_node = models.StartNode(
#     id=4,
#     node_type=NodeTypes.MESSAGE,
# )
#
# mock_data_existing2 = models.MessageNode(
#     id=mock_data_existing2_node.id,
#     status=MessageStatuses.PENDING,
#     text="Existing message node 2",
#     parent_node_id=2,
#     parent_condition_edge_id=0,
#     workflow_id=1,
# )
#
#
# engine = create_engine(
#     "sqlite:///:memory:", connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # Create tables in the in-memory database
# models.Base.metadata.create_all(bind=engine)
# db = SessionLocal()
#
# db.add_all(
#     [
#         mock_data_start,
#         mock_data_start_node,
#         mock_data_start2,
#         mock_data_start2_node,
#         mock_data_existing,
#         mock_data_existing_node,
#         mock_data_existing2,
#         mock_data_existing2_node,
#     ]
# )
#
# db.commit()
#
#
# # @pytest.fixture
# # def override_get_db():
# #     try:
# #         yield SessionLocal
# #     finally:
# #         SessionLocal.close_all()
#
#
# def override_get_db():
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)

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


engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # File-based database
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = scoped_session(SessionLocal)
#
# Base.metadata.create_all(bind=engine)

# Create a scoped session
db = scoped_session(SessionLocal)

# Load mock data from a JSON file
current_dir = os.path.dirname(__file__)

# Construct the absolute path to the file
file_path = os.path.join(current_dir, "mock_db_for_tests.json")

with open(file_path, "r") as f:
    mock_data = json.load(f)

# Insert mock data into the database
insert_mock_data(db, mock_data)

db.commit()


# Override the get_db dependency in your app
def override_get_db():
    try:
        yield db
    finally:
        db.remove()


app.dependency_overrides[get_db] = override_get_db

# Create a TestClient
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
