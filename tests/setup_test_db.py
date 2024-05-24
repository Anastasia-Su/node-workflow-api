import json
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, session

from tests.mock_models import (
    EndNode,
    ConditionNode,
    StartNode,
    MessageNode,
    Base,
    Workflow,
    ConditionEdge,
    Node,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def setup_test_db(db):
    # current_dir = os.path.dirname(__file__)
    # file_path = os.path.join(current_dir, "mock_db.json")
    file_path = "mock_db.json"
    with open(file_path, "r") as f:
        mock_data = json.load(f)

    for workflow_data in mock_data:
        start_nodes = workflow_data.get("start_nodes", [])
        message_nodes = workflow_data.get("message_nodes", [])
        condition_nodes = workflow_data.get("condition_nodes", [])
        end_nodes = workflow_data.get("end_nodes", [])
        workflows = workflow_data.get("workflows", [])
        condition_edges = workflow_data.get("condition_edges", [])

        for start_node_data in start_nodes:
            start_node = StartNode(
                id=start_node_data["id"],
                message=start_node_data["message"],
                workflow_id=start_node_data["workflow_id"],
            )
            db.add(start_node)

        for message_node_data in message_nodes:
            message_node = MessageNode(
                id=message_node_data["id"],
                status=message_node_data["status"],
                text=message_node_data["text"],
                parent_node_id=message_node_data["parent_node_id"],
                parent_condition_edge_id=message_node_data[
                    "parent_condition_edge_id"
                ],
                workflow_id=message_node_data["workflow_id"],
            )
            db.add(message_node)

        for condition_node_data in condition_nodes:
            condition_node = ConditionNode(
                id=condition_node_data["id"],
                condition=condition_node_data["condition"],
                parent_node_id=condition_node_data["parent_node_id"],
                parent_message_node_id=condition_node_data[
                    "parent_message_node_id"
                ],
                workflow_id=condition_node_data["workflow_id"],
            )
            db.add(condition_node)

        for end_node_data in end_nodes:
            end_node = EndNode(
                id=end_node_data["id"],
                message=end_node_data["message"],
                parent_node_id=end_node_data["parent_node_id"],
                workflow_id=end_node_data["workflow_id"],
            )
            db.add(end_node)

        for w_data in workflows:
            workflow = Workflow(id=w_data["id"], name=w_data["name"])
            db.add(workflow)

        for edge_data in condition_edges:
            c_edge = ConditionEdge(
                id=edge_data["id"],
                condition_node_id=edge_data["condition_node_id"],
                edge=edge_data["edge"],
            )
            db.add(c_edge)

    db.commit()
    return db
