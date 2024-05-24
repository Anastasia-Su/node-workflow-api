from fastapi import APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_end
from nodes.routers.exceptions_for_routers.exceptions import (
    exceptions_for_router_404,
    exceptions_for_end_router_403,
)

router = APIRouter()


@router.get("/end_nodes/", response_model=list[schemas.EndNode])
def read_end_nodes(
    db: CommonDB,
) -> list[models.EndNode]:
    """Endpoint for retrieving all end nodes"""

    return crud_end.get_end_node_list(db=db)


@router.get("/end_nodes/{end_node_id}/", response_model=schemas.EndNode)
def read_single_end_node(end_node_id: int, db: CommonDB) -> models.EndNode:
    """Endpoint for retrieving a single end node"""

    db_node = crud_end.get_end_node_detail(db=db, node_id=end_node_id)

    exceptions_for_router_404(db_node=db_node, node_id=end_node_id)

    return db_node


@router.post("/end_nodes/", response_model=schemas.EndNodeCreate)
def create_end_node_endpoint(
    end_node: schemas.EndNodeCreate,
    db: CommonDB,
) -> models.EndNode:
    """Endpoint for creating an end node"""

    exceptions_for_end_router_403(end_node=end_node, db=db)

    return crud_end.create_end_node(db=db, node=end_node)


@router.put(
    "/end_nodes/{end_node_id}",
    response_model=schemas.EndNodeCreate,
)
def update_end_node_endpoint(
    node_id: int, node: schemas.EndNodeCreate, db: CommonDB
) -> models.EndNode:
    """Endpoint for updating an end node"""

    exceptions_for_end_router_403(end_node=node, db=db)

    db_node = crud_end.update_end_node(
        db=db,
        node_id=node_id,
        new_node=node,
    )

    exceptions_for_router_404(db_node=db_node, node_id=node_id)

    return db_node


@router.delete("/end_nodes/{end_node_id}", response_model=schemas.EndNode)
def delete_end_node(node_id: int, db: CommonDB) -> models.EndNode:
    """Endpoint for deleting an end node"""

    db_node = crud_end.delete_end_node(db=db, node_id=node_id)

    exceptions_for_router_404(db_node=db_node, node_id=node_id)

    return db_node
