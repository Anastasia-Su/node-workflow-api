import json
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database_setup import SessionLocal, engine


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from src.nodes import models
from src.nodes.models import Base


load_dotenv()


def truncate_tables(db: SessionLocal) -> None:
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        db.execute(table.delete())
    db.commit()


def insert_mock_data(db: SessionLocal, file_name: str) -> None:
    with open(file_name, "r") as f:
        mock_data = json.load(f)
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for workflow_data in mock_data:
            start_nodes = workflow_data.get("start_nodes", [])
            message_nodes = workflow_data.get("message_nodes", [])
            condition_nodes = workflow_data.get("condition_nodes", [])
            end_nodes = workflow_data.get("end_nodes", [])
            workflows = workflow_data.get("workflows", [])
            condition_edges = workflow_data.get("condition_edges", [])

            for w_data in workflows:
                workflow = models.Workflow(
                    id=w_data["id"], name=w_data["name"]
                )
                db.add(workflow)

            for edge_data in condition_edges:
                c_edge = models.ConditionEdge(
                    id=edge_data["id"],
                    condition_node_id=edge_data["condition_node_id"],
                    edge=edge_data["edge"],
                )
                db.add(c_edge)

            for start_node_data in start_nodes:
                start_node = models.StartNode(
                    id=start_node_data["id"],
                    message=start_node_data["message"],
                    workflow_id=start_node_data["workflow_id"],
                )
                db.add(start_node)

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
                )
                db.add(message_node)

            for condition_node_data in condition_nodes:
                condition_node = models.ConditionNode(
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
                end_node = models.EndNode(
                    id=end_node_data["id"],
                    message=end_node_data["message"],
                    parent_node_id=end_node_data["parent_node_id"],
                    workflow_id=end_node_data["workflow_id"],
                )
                db.add(end_node)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error inserting mock data: {e}")
    finally:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))


if __name__ == "__main__":
    filename = sys.argv[1]

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        truncate_tables(db)
        insert_mock_data(db, filename)
        print("Mock data loaded successfully.")

    finally:
        db.close()
