from sqlalchemy import and_
from sqlalchemy.orm import Session
from nodes import models, schemas


def get_condition_node_list(
    db: Session,
    parent_message_node_id: int | None = None,
    condition: str | None = None,
) -> list[type(models.ConditionNode)]:
    """Retrieve all condition nodes with the option to filter by parent_message_id and condition."""

    condition_nodes = db.query(models.ConditionNode)

    filters = []
    if parent_message_node_id is not None:
        filters.append(
            models.ConditionNode.parent_message_node_id
            == parent_message_node_id
        )

    if condition is not None:
        filters.append(models.ConditionNode.condition.ilike(f"%{condition}%"))

    if filters:
        condition_nodes = condition_nodes.filter(and_(*filters))

    return condition_nodes.all()


def get_condition_node_detail(
    db: Session, node_id: int
) -> models.ConditionNode:
    """Retrieve a condition node with the given id."""

    return db.query(models.ConditionNode).get(node_id)


def create_condition_node(
    db: Session, node: schemas.ConditionNodeCreate
) -> models.ConditionNode:
    """Create a new condition node."""

    db_node = models.ConditionNode(
        condition=node.condition,
        parent_node_id=node.parent_node_id,
        parent_message_node_id=node.parent_message_node_id,
        workflow_id=node.workflow_id,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_condition_node(
    db: Session, node_id: int, new_node: schemas.ConditionNodeCreate
) -> type(models.ConditionNode):
    """Update a condition node with the given id."""

    node = db.get(models.ConditionNode, node_id)

    if node:
        node.condition = new_node.condition
        node.parent_node_id = new_node.parent_node_id
        node.parent_message_node_id = new_node.parent_message_node_id
        node.workflow_id = new_node.workflow_id

        db.commit()
        db.refresh(node)

    return node


def delete_condition_node(
    db: Session, node_id: int
) -> type(models.ConditionNode):
    """Delete a condition node."""

    node = db.get(models.ConditionNode, node_id)

    if node:
        db.delete(node)
        db.commit()

    return node
