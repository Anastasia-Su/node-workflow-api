from sqlalchemy.orm import Session
from nodes import models, schemas


def get_workflow_list(db: Session) -> list[models.WorkflowNode]:
    return db.query(models.WorkflowNode).all()


def get_workflow_detail(db: Session, node_id: int) -> models.WorkflowNode:
    return db.query(models.WorkflowNode).get(node_id)


def create_workflow(
    db: Session, node: schemas.WorkflowNodeCreate
) -> models.WorkflowNode:
    db_node = models.WorkflowNode(
        start_node_id=node.start_node,
        message_node_id=node.message_node,
        condition_node_id=node.condition_node,
        end_node_id=node.end_node,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_workflow(
    db: Session,
    node_id: int,
    new_start_node: int,
    new_message_node: int,
    new_condition_node: int,
    new_end_node: int,
):
    node = db.get(models.WorkflowNode, node_id)
    if node:
        node.start_node_id = (new_start_node,)
        node.message_node_id = (new_message_node,)
        node.condition_node_id = (new_condition_node,)
        node.end_node_id = (new_end_node,)
        db.commit()
        db.refresh(node)

    return node


def delete_workflow(db: Session, node_id: int):
    node = db.get(models.WorkflowNode, node_id)
    if node:
        db.delete(node)
        db.commit()

    return node
