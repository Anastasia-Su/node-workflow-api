from fastapi import APIRouter, Query

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_condition, crud_condition_edge
from nodes.models import ConditionEdges
from nodes.routers.utils_for_routers import (
    exceptions_for_router_404,
    exceptions_for_condition_router_403,
)

router = APIRouter()


@router.get("/condition_nodes/", response_model=list[schemas.ConditionNode])
def read_condition_nodes(
    db: CommonDB,
    parent_message_node_id: int | None = Query(
        None, description="Filter by parent_message_node_id"
    ),
    condition: str | None = Query(
        None, description="Filter by piece of condition"
    ),
) -> list[models.ConditionNode]:
    """Endpoint for retrieving all condition nodes with filter options"""

    return crud_condition.get_condition_node_list(
        db=db,
        parent_message_node_id=parent_message_node_id,
        condition=condition,
    )


@router.get(
    "/condition_nodes/{condition_node_id}/",
    response_model=schemas.ConditionNode,
)
def read_single_condition_node(
    condition_node_id: int, db: CommonDB
) -> models.ConditionNode:
    """Endpoint for retrieving a single condition node"""

    db_condition_node = crud_condition.get_condition_node_detail(
        db=db, node_id=condition_node_id
    )

    exceptions_for_router_404(
        db_node=db_condition_node, node_id=condition_node_id
    )

    return db_condition_node


@router.post("/condition_nodes/", response_model=schemas.ConditionNodeCreate)
def create_condition_node_endpoint(
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
) -> models.ConditionNode:
    """Endpoint for creating a condition node"""

    exceptions_for_condition_router_403(condition_node=condition_node, db=db)

    new_condition_node = crud_condition.create_condition_node(
        db=db, node=condition_node
    )

    crud_condition_edge.create_condition_edge(
        db=db,
        edge=schemas.ConditionEdgeCreate(
            condition_node_id=new_condition_node.id, edge=ConditionEdges.YES
        ),
    )

    crud_condition_edge.create_condition_edge(
        db=db,
        edge=schemas.ConditionEdgeCreate(
            condition_node_id=new_condition_node.id, edge=ConditionEdges.NO
        ),
    )

    return new_condition_node


@router.put(
    "/condition_nodes/{condition_node_id}",
    response_model=schemas.ConditionNodeCreate,
)
def update_condition_node_endpoint(
    node_id: int,
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
) -> models.ConditionNode:
    """Endpoint for updating a condition node"""

    exceptions_for_condition_router_403(condition_node=condition_node, db=db)

    db_condition_node = crud_condition.update_condition_node(
        db=db, node_id=node_id, new_node=condition_node
    )

    exceptions_for_router_404(db_node=db_condition_node, node_id=node_id)

    return db_condition_node


@router.delete(
    "/condition_nodes/{condition_node_id}",
    response_model=schemas.ConditionNode,
)
def delete_condition_node(node_id: int, db: CommonDB) -> models.ConditionNode:
    """Endpoint for deleting a condition node"""

    db_node = crud_condition.delete_condition_node(db=db, node_id=node_id)

    exceptions_for_router_404(db_node=db_node, node_id=node_id)

    return db_node
