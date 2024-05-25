from sqlalchemy import and_
from sqlalchemy.orm import Session
from nodes import models, schemas
from nodes.models import MessageStatuses


def get_message_node_list(
    db: Session,
    text: str | None = None,
    message_status: MessageStatuses | None = None,
) -> list[type(models.MessageNode)]:
    """Retrieve all message nodes with the option to filter by text and status"""

    message_nodes = db.query(models.MessageNode)

    filters = []
    if message_status is not None:
        filters.append(models.MessageNode.status == message_status)
    if text is not None:
        filters.append(models.MessageNode.text.ilike(f"%{text}%"))

    if filters:
        message_nodes = message_nodes.filter(and_(*filters))

    return message_nodes.all()


def get_message_node_detail(
    db: Session, node_id: int
) -> type(models.MessageNode):
    """Retrieve a message node with the given id"""

    return db.get(models.MessageNode, node_id)


def create_message_node(
    db: Session, node: schemas.MessageNodeCreate
) -> models.MessageNode:
    """Create a new message node"""

    db_node = models.MessageNode(
        status=node.status,
        text=node.text,
        parent_node_id=node.parent_node_id,
        parent_condition_edge_id=node.parent_condition_edge_id,
        workflow_id=node.workflow_id,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_message_node(
    db: Session, node_id: int, new_node: schemas.MessageNodeCreate
) -> type(models.MessageNode):
    """Update a message node with the given id"""

    node = db.get(models.MessageNode, node_id)

    if node:
        node.status = new_node.status
        node.text = new_node.text
        node.parent_node_id = new_node.parent_node_id
        node.parent_condition_edge_id = new_node.parent_condition_edge_id
        node.workflow_id = new_node.workflow_id

        db.commit()
        db.refresh(node)

    return node


def delete_message_node(db: Session, node_id: int) -> type(models.MessageNode):
    """Delete a message node with the given id"""

    node = db.get(models.MessageNode, node_id)
    if node:
        db.delete(node)
        db.commit()

    return node
