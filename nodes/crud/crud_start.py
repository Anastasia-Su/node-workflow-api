from sqlalchemy.orm import Session
from nodes import models, schemas


def get_start_node_list(db: Session) -> list[models.StartNode]:
    return db.query(models.StartNode).all()


def get_start_node_detail(db: Session, node_id: int) -> models.StartNode:
    return db.query(models.StartNode).get(node_id)


def create_start_node(
    db: Session, node: schemas.StartNodeCreate
) -> models.StartNode:

    db_node = models.StartNode(
        message=node.message, message_node_id=node.message_node_id
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_start_node(
    db: Session,
    node_id: int,
    new_message: str,
    new_message_node_id: int | None,
) -> models.StartNode:
    node = db.get(models.StartNode, node_id)
    if node:
        node.message = new_message
        node.message_node_id = new_message_node_id
        db.commit()
        db.refresh(node)

    return node


def delete_start_node(db: Session, node_id: int):
    node = db.get(models.StartNode, node_id)
    if node:
        db.delete(node)
        db.commit()
    return node
