from sqlalchemy.orm import Session
from nodes import models, schemas


def get_end_node_list(db: Session) -> list[type(models.EndNode)]:
    """Retrieve all end nodes"""

    return db.query(models.EndNode).all()


def get_end_node_detail(db: Session, node_id: int) -> models.EndNode:
    """Retrieve an end node with the given id"""

    return db.query(models.EndNode).get(node_id)


def create_end_node(
    db: Session, node: schemas.EndNodeCreate
) -> models.EndNode:
    """Create an end node"""

    db_node = models.EndNode(
        message=node.message,
        parent_node_id=node.parent_node_id,
        workflow_id=node.workflow_id,
    )

    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_end_node(
    db: Session,
    node_id: int,
    new_node: schemas.EndNodeCreate,
) -> type(models.EndNode):
    """Update an end node with the given id"""

    node = db.get(models.EndNode, node_id)

    if node:
        node.message = new_node.message
        node.parent_node_id = new_node.parent_node_id
        node.workflow_id = new_node.workflow_id

        db.commit()
        db.refresh(node)

    return node


def delete_end_node(db: Session, node_id: int) -> type(models.EndNode):
    """Delete an end node with the given id"""

    node = db.get(models.EndNode, node_id)

    if node:
        db.delete(node)
        db.commit()

    return node
