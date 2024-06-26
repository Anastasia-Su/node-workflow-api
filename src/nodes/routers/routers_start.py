from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from database.dependencies import CommonDB
from src.nodes import models, schemas
from src.nodes.crud import crud_start
from src.nodes.routers.exceptions_for_routers.exceptions import (
    exceptions_for_router_404,
    exceptions_for_start_router_403,
)

router = APIRouter()


@router.get("/start_nodes/", response_model=list[schemas.StartNode])
def read_start_nodes(
    db: CommonDB,
) -> list[models.StartNode]:
    """Endpoint for retrieving all start nodes"""

    return crud_start.get_start_node_list(db=db)


@router.get("/start_nodes/{node_id}/", response_model=schemas.StartNode)
def read_single_start_node(node_id: int, db: CommonDB) -> models.StartNode:
    """Endpoint for retrieving a single start node"""

    db_start_node = crud_start.get_start_node_detail(db=db, node_id=node_id)

    exceptions_for_router_404(db_node=db_start_node, node_id=node_id)

    return db_start_node


@router.post("/start_nodes/", response_model=schemas.StartNodeCreate)
def create_start_node_endpoint(
    start_node: schemas.StartNodeCreate,
    db: CommonDB,
) -> models.StartNode:
    """Endpoint for creating a start node"""

    exceptions_for_start_router_403(start_node=start_node, db=db)

    return crud_start.create_start_node(db=db, node=start_node)


@router.put(
    "/start_nodes/{node_id}",
    response_model=schemas.StartNodeCreate,
)
def update_start_node_endpoint(
    node_id: int, node: schemas.StartNodeCreate, db: CommonDB
) -> type(models.StartNode):
    """Endpoint for updating a start node"""

    try:
        db_node = crud_start.update_start_node(
            db=db,
            node_id=node_id,
            new_node=node,
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error. Please check workflow id.",
        )

    exceptions_for_router_404(db_node=db_node, node_id=node_id)
    exceptions_for_start_router_403(start_node=node, db=db)

    return db_node


@router.delete("/start_nodes/{node_id}", response_model=schemas.StartNode)
def delete_start_node(node_id: int, db: CommonDB) -> type(models.StartNode):
    """Endpoint for deleting a start node"""

    db_node = crud_start.delete_start_node(db=db, node_id=node_id)
    exceptions_for_router_404(db_node=db_node, node_id=node_id)

    return db_node
