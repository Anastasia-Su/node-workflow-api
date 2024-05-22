from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_condition_edge
from nodes.routers.utils_for_routers import (
    exceptions_for_router_404,
    exception_for_wrong_ref_id,
    exceptions_for_condition_edge_router_403,
)

router = APIRouter()


@router.get("/condition_edges/", response_model=list[schemas.ConditionEdge])
def read_condition_edges(
    db: CommonDB,
) -> list[models.ConditionEdge]:
    """Endpoint for retrieving all condition edges"""

    return crud_condition_edge.get_condition_edge_list(db=db)


@router.get(
    "/condition_edges/{condition_edge_id}/",
    response_model=schemas.ConditionEdge,
)
def read_single_condition_edge(
    condition_edge_id: int, db: CommonDB
) -> models.ConditionEdge:
    """Endpoint for retrieving a single condition edge"""

    db_condition_edge = crud_condition_edge.get_condition_edge_detail(
        db=db, edge_id=condition_edge_id
    )

    exceptions_for_router_404(
        db_node=db_condition_edge, node_id=condition_edge_id
    )

    return db_condition_edge


@router.put(
    "/condition_edges/{condition_edge_id}",
    response_model=schemas.ConditionEdgeCreate,
)
def update_condition_edge_endpoint(
    edge_id: int, edge: schemas.ConditionEdgeCreate, db: CommonDB
) -> models.ConditionEdge:
    """Endpoint for updating a condition edge"""

    exceptions_for_condition_edge_router_403(edge=edge, db=db)

    db_edge = crud_condition_edge.update_condition_edge(
        db=db, edge_id=edge_id, new_edge=edge
    )

    exceptions_for_router_404(db_node=db_edge, node_id=edge_id)

    return db_edge


@router.delete(
    "/condition_edges/{condition_edge_id}",
    response_model=schemas.ConditionEdge,
)
def delete_condition_edge(edge_id: int, db: CommonDB) -> models.ConditionEdge:
    """Endpoint for deleting a condition edge"""

    db_edge = crud_condition_edge.delete_condition_edge(db=db, edge_id=edge_id)

    exceptions_for_router_404(db_node=db_edge, node_id=edge_id)

    return db_edge
