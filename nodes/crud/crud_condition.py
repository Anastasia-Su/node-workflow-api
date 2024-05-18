from sqlalchemy.orm import Session
from nodes import models, schemas


def get_condition_node_list(db: Session) -> list[models.ConditionNode]:
    return db.query(models.ConditionNode).all()


def get_condition_node_detail(
    db: Session, node_id: int
) -> models.ConditionNode:
    return db.query(models.ConditionNode).get(node_id)


def create_condition_node(
    db: Session, node: schemas.ConditionNodeCreate
) -> models.ConditionNode:
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
):
    node = db.get(models.ConditionNode, node_id)
    if node:
        node.condition = new_node.condition
        node.edge = new_node.edge
        node.parent_node_id = new_node.parent_node_id
        node.parent_message_node_id = new_node.parent_message_node_id
        node.workflow_id = new_node.workflow_id

        db.commit()
        db.refresh(node)

    return node


def delete_condition_node(db: Session, node_id: int):
    node = db.get(models.ConditionNode, node_id)
    if node:
        db.delete(node)
        db.commit()

    return node
