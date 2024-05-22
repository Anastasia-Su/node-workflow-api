from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_condition_edge

router = APIRouter()


@router.get("/condition_edges/", response_model=list[schemas.ConditionEdge])
def read_condition_edges(
    db: CommonDB,
) -> list[models.ConditionEdge]:

    return crud_condition_edge.get_condition_edge_list(db=db)


@router.get(
    "/condition_edges/{condition_edge_id}/",
    response_model=schemas.ConditionEdge,
)
def read_single_condition_edge(
    condition_edge_id: int, db: CommonDB
) -> models.ConditionEdge:
    db_condition_edge = crud_condition_edge.get_condition_edge_detail(
        db=db, edge_id=condition_edge_id
    )

    if db_condition_edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")

    return db_condition_edge


@router.put(
    "/condition_edges/{condition_edge_id}",
    response_model=schemas.ConditionEdgeCreate,
)
def update_condition_edge_endpoint(
    edge_id: int, edge: schemas.ConditionEdgeCreate, db: CommonDB
):
    condition_node = crud_condition_edge.get_condition_edge_detail(
        db=db, edge_id=edge_id
    )

    if not condition_node:
        raise HTTPException(
            status_code=404,
            detail=f"Edge with id {edge.condition_node_id} not found",
        )

    db_edge = crud_condition_edge.update_condition_edge(
        db=db, edge_id=edge_id, new_edge=edge
    )

    if db_edge is None:
        raise HTTPException(
            status_code=404, detail=f"Edge with id {edge_id} not found"
        )

    return db_edge


@router.delete(
    "/condition_edges/{condition_edge_id}",
    response_model=schemas.ConditionEdge,
)
def delete_condition_edge(edge_id: int, db: CommonDB):
    db_edge = crud_condition_edge.delete_condition_edge(db=db, edge_id=edge_id)
    if db_edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")

    return db_edge
