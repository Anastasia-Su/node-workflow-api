import json

from sqlalchemy.orm import Session
from nodes import models, schemas


def get_workflow_list(db: Session) -> list[type(models.Workflow)]:
    """Retrieve all workflows"""

    return db.query(models.Workflow).all()


def get_workflow_detail(db: Session, node_id: int) -> models.Workflow:
    """Retrieve a workflow with the given id"""

    node = db.query(models.Workflow).get(node_id)

    return node


def create_workflow(
    db: Session, node: schemas.WorkflowCreate
) -> models.Workflow:
    """Create a new workflow"""

    db_node = models.Workflow(
        name=node.name,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_workflow(
    db: Session, node_id: int, new_node: schemas.WorkflowCreate
) -> type(models.Workflow):
    """Update a workflow with the given id"""

    node = db.get(models.Workflow, node_id)

    if node:
        node.name = new_node.name

        db.commit()
        db.refresh(node)

    return node


def delete_workflow(db: Session, node_id: int) -> type(models.Workflow):
    """Delete a workflow with the given id"""

    node = db.get(models.Workflow, node_id)

    if node:
        db.delete(node)
        db.commit()

    return node
