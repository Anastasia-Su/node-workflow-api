from sqlalchemy.orm import Session
from nodes import models, schemas


def get_start_node_list(db: Session) -> list[type(models.StartNode)]:
    """Retrieve all start nodes"""

    return db.query(models.StartNode).all()


def get_start_node_detail(db: Session, node_id: int) -> models.StartNode:
    """Retrieve a start node with the given id"""
    return db.query(models.StartNode).get(node_id)


def create_start_node(
    db: Session, node: schemas.StartNodeCreate
) -> models.StartNode:
    """Create a new start node"""

    db_node = models.StartNode(
        message=node.message, workflow_id=node.workflow_id
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_start_node(
    db: Session,
    node_id: int,
    new_node: schemas.StartNodeCreate,
) -> type(models.StartNode):
    """Update a start node with the given id"""

    node = db.get(models.StartNode, node_id)
    if node:
        node.message = new_node.message
        node.workflow_id = new_node.workflow_id

        db.commit()
        db.refresh(node)

    return node


def delete_start_node(db: Session, node_id: int) -> type(models.StartNode):
    """Delete a start node with the given id"""

    node = db.get(models.StartNode, node_id)
    if node:
        db.delete(node)
        db.commit()
    return node
