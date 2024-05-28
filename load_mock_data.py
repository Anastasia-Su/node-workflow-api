import json
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from database import Base
from nodes import models

load_dotenv()

# SQLALCHEMY_DATABASE_URL = os.environ["SQLITE_DATABASE_URL"]
SQLALCHEMY_DATABASE_URL = os.environ["MARIADB_DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def truncate_tables(db):
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        db.execute(table.delete())
    db.commit()


def insert_mock_data(db, file_name):
    with open(file_name, "r") as f:
        mock_data = json.load(f)

    for workflow_data in mock_data:
        start_nodes = workflow_data.get("start_nodes", [])
        message_nodes = workflow_data.get("message_nodes", [])
        condition_nodes = workflow_data.get("condition_nodes", [])
        end_nodes = workflow_data.get("end_nodes", [])
        workflows = workflow_data.get("workflows", [])
        condition_edges = workflow_data.get("condition_edges", [])

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

        for start_node_data in start_nodes:
            start_node = models.StartNode(
                id=start_node_data["id"],
                message=start_node_data["message"],
                workflow_id=start_node_data["workflow_id"],
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
            )
            db.add(condition_node)
            db.commit()

        for end_node_data in end_nodes:
            end_node = models.EndNode(
                id=end_node_data["id"],
                message=end_node_data["message"],
                parent_node_id=end_node_data["parent_node_id"],
                workflow_id=end_node_data["workflow_id"],
            )
            db.add(end_node)
            db.commit()

    db.commit()


if __name__ == "__main__":
    filename = sys.argv[1]

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # SQLALCHEMY_DATABASE_URL = f"{os.environ.get('MARIADB_DATABASE_ROOT')}/test"
    #
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    #
    # if not database_exists(engine.url):
    #     create_database(engine.url)
    #
    # TestingSessionLocal = sessionmaker(
    #     autocommit=False, autoflush=False, bind=engine
    # )
    # Base.metadata.create_all(bind=engine)
    #
    # db = TestingSessionLocal()

    try:
        truncate_tables(db)
        insert_mock_data(db, filename)
        print("Mock data loaded successfully.")

    finally:
        db.close()
