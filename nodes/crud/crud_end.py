from sqlalchemy.orm import Session
from nodes import models, schemas


def get_end_node_list(db: Session) -> list[models.EndNode]:
    return db.query(models.EndNode).all()


def get_end_node_detail(db: Session, node_id: int) -> models.EndNode:
    return db.query(models.EndNode).get(node_id)


def create_end_node(
    db: Session, node: schemas.EndNodeCreate
) -> models.EndNode:
    db_node = models.EndNode(
        message=node.message, message_node_id=node.message_node_id
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def update_end_node(
    db: Session,
    node_id: int,
    new_message: str,
    new_message_node_id: int | None,
):
    node = db.get(models.EndNode, node_id)
    if node:
        node.message = new_message
        node.new_message_node_id = new_message_node_id
        db.commit()
        db.refresh(node)
    return node


def delete_end_node(db: Session, node_id: int):
    node = db.get(models.EndNode, node_id)
    if node:
        db.delete(node)
        db.commit()
    return node
