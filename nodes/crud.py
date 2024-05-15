from sqlalchemy.orm import Session
from nodes import models
from nodes import schemas


def get_message_node_list(db: Session) -> list[models.MessageNode]:
    return db.query(models.MessageNode).all()


def get_message_node_detail(db: Session, node_id: int) -> models.MessageNode:
    return db.query(models.MessageNode).get(node_id)


def create_message_node(
    db: Session, node: schemas.MessageNodeCreate
) -> models.MessageNode:
    db_node = models.MessageNode(
        status=node.status,
        text=node.text,
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node
