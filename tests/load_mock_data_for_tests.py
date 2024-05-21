import json
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from nodes import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./node-workflow.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_mock_data(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def insert_mock_data(db, data):
    for workflow_data in data:
        start_nodes = workflow_data.get("start_nodes", [])
        message_nodes = workflow_data.get("message_nodes", [])
        condition_nodes = workflow_data.get("condition_nodes", [])
        end_nodes = workflow_data.get("end_nodes", [])
        workflows = workflow_data.get("workflows", [])
        condition_edges = workflow_data.get("condition_edges", [])

        for start_node_data in start_nodes:
            start_node = models.StartNode(
                id=start_node_data["id"],
                message=start_node_data["message"],
                workflow_id=start_node_data["workflow_id"],
                node_type=start_node_data["node_type"],
            )
            db.add(start_node)
            db.commit()

        for message_node_data in message_nodes:
            message_node = models.MessageNode(
                id=message_node_data["id"],
                status=message_node_data["status"],
                text=message_node_data["text"],
                parent_node_id=message_node_data["parent_node_id"],
                parent_condition_edge_id=message_node_data[
                    "parent_condition_edge_id"
                ],
                workflow_id=message_node_data["workflow_id"],
                node_type=message_node_data["node_type"],
            )
            db.add(message_node)
            db.commit()

        for condition_node_data in condition_nodes:
            condition_node = models.ConditionNode(
                id=condition_node_data["id"],
                condition=condition_node_data["condition"],
                parent_node_id=condition_node_data["parent_node_id"],
                parent_message_node_id=condition_node_data[
                    "parent_message_node_id"
                ],
                workflow_id=condition_node_data["workflow_id"],
                node_type=condition_node_data["node_type"],
            )
            db.add(condition_node)
            db.commit()

        for end_node_data in end_nodes:
            end_node = models.EndNode(
                id=end_node_data["id"],
                message=end_node_data["message"],
                parent_node_id=end_node_data["parent_node_id"],
                workflow_id=end_node_data["workflow_id"],
                node_type=end_node_data["node_type"],
            )
            db.add(end_node)
            db.commit()

        for w_data in workflows:
            workflow = models.Workflow(id=w_data["id"], name=w_data["name"])
            db.add(workflow)
            db.commit()

        for edge_data in condition_edges:
            c_edge = models.ConditionEdge(
                id=edge_data["id"],
                condition_node_id=edge_data["condition_node_id"],
                edge=edge_data["edge"],
            )
            db.add(c_edge)
            db.commit()
