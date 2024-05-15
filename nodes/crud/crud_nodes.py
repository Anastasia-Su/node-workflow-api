from sqlalchemy.orm import Session
from nodes import models, schemas
from nodes.models import Node, association_table


def get_node_list(db: Session) -> list[models.Node]:
    return db.query(models.Node).all()


def get_node_detail(db: Session, node_id: int):
    return db.query(Node).filter(Node.id == node_id).first()


def create_node(db: Session, type: str):
    new_node = Node(type=type)

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node


def update_node(db: Session, node_id: int, new_type: str):
    node = db.get(models.Node, node_id)
    if node:
        node.type = new_type
        db.commit()
        db.refresh(node)
    return node


def delete_node(db: Session, node_id: int):
    node = db.get(models.Node, node_id)
    if node:
        db.delete(node)
        db.commit()
    return node


def get_associations_list(db: Session):
    return db.query(models.Node.incoming_nodes).all()


def get_associations_for_node(db: Session, node_id: int):
    return db.query(Node).filter(Node.id == node_id).first().incoming_nodes


def create_association(db: Session, source_node_id: int, target_node_id: int):
    association = association_table.insert().values(
        source_id=source_node_id, target_id=target_node_id
    )
    db.execute(association)
    db.commit()


def delete_association(db: Session, source_node_id: int, target_node_id: int):
    association = (
        association_table.delete()
        .where(association_table.c.source_id == source_node_id)
        .where(association_table.c.target_id == target_node_id)
    )
    db.execute(association)
    db.commit()
