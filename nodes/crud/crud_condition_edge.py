from sqlalchemy.orm import Session
from nodes import models, schemas


def get_condition_edge_list(db: Session) -> list[models.ConditionEdge]:
    return db.query(models.ConditionEdge).all()


def get_condition_edge_detail(
    db: Session, edge_id: int
) -> models.ConditionEdge:
    return db.query(models.ConditionEdge).get(edge_id)


def create_condition_edge(
    db: Session, edge: schemas.ConditionEdgeCreate
) -> models.ConditionEdge:
    db_edge = models.ConditionEdge(
        edge=edge.edge,
        condition_node_id=edge.condition_node_id,
    )
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)

    return db_edge


def update_condition_edge(
    db: Session, edge_id: int, new_edge: schemas.ConditionEdgeCreate
):
    edge = db.get(models.ConditionEdge, edge_id)
    if edge:
        edge.edge = new_edge.edge
        edge.condition_node_id = new_edge.condition_node_id

        db.commit()
        db.refresh(edge)

    return edge


def delete_condition_edge(db: Session, edge_id: int):
    edge = db.get(models.ConditionEdge, edge_id)
    if edge:
        db.delete(edge)
        db.commit()
    return edge
