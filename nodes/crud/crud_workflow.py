from sqlalchemy.orm import Session
from nodes import models, schemas


def get_workflow_list(db: Session) -> list[models.WorkflowNode]:
    return db.query(models.WorkflowNode).all()


def get_workflow_detail(db: Session, node_id: int) -> models.WorkflowNode:
    return db.query(models.WorkflowNode).get(node_id)


def create_workflow(
    db: Session, node: schemas.WorkflowNodeCreate
) -> models.WorkflowNode:

    message_node_ids_str = ",".join(map(str, node.message_node_ids))
    condition_node_ids_str = ",".join(map(str, node.condition_node_ids))

    db_node = models.WorkflowNode(
        start_node_id=node.start_node_id,
        message_node_ids=message_node_ids_str,
        condition_node_ids=condition_node_ids_str,
        end_node_id=node.end_node_id,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    message_node_ids_list = [
        int(id_str) for id_str in message_node_ids_str.split(",")
    ]
    condition_node_ids_list = [
        int(id_str) for id_str in condition_node_ids_str.split(",")
    ]

    # Update the workflow node object with the lists
    db_node.message_node_ids = message_node_ids_list
    db_node.condition_node_ids = condition_node_ids_list

    return db_node


def update_workflow(
    db: Session,
    node_id: int,
    new_start_node: int,
    new_message_nodes: str,
    new_condition_nodes: str,
    new_end_node: int,
):

    node = db.get(models.WorkflowNode, node_id)

    if node:
        node.start_node_id = (new_start_node,)
        node.message_node_ids = (new_message_nodes,)
        node.condition_node_ids = (new_condition_nodes,)
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
