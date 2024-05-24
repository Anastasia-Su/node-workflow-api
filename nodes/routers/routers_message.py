from fastapi import APIRouter, Query

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_message
from nodes.models import MessageStatuses
from nodes.routers.exceptions_for_routers.exceptions import (
    exceptions_for_message_router_403,
    exceptions_for_router_404,
)

router = APIRouter()


@router.get("/message_nodes/", response_model=list[schemas.MessageNode])
def read_message_nodes(
    db: CommonDB,
    text: str | None = Query(None, description="Filter by piece of text"),
    status: MessageStatuses | None = Query(
        None, description="Filter by status"
    ),
) -> list[models.MessageNode]:
    """Endpoint for retrieving all message nodes with filter options"""

    return crud_message.get_message_node_list(
        db=db, text=text, message_status=status
    )


@router.get(
    "/message_nodes/{message_node_id}/", response_model=schemas.MessageNode
)
def read_single_message_node(
    message_node_id: int, db: CommonDB
) -> models.MessageNode:
    """Endpoint for retrieving a single messages node"""

    db_message_node = crud_message.get_message_node_detail(
        db=db, node_id=message_node_id
    )

    exceptions_for_router_404(db_node=db_message_node, node_id=message_node_id)

    return db_message_node


@router.post("/message_nodes/", response_model=schemas.MessageNodeCreate)
def create_message_node_endpoint(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
) -> models.MessageNode:
    """Endpoint for creating a messages node"""

    exceptions_for_message_router_403(message_node=message_node, db=db)

    return crud_message.create_message_node(db=db, node=message_node)


@router.put(
    "/message_nodes/{message_node_id}",
    response_model=schemas.MessageNodeCreate,
)
def update_message_node_endpoint(
    message_node_id: int, message_node: schemas.MessageNodeCreate, db: CommonDB
) -> models.MessageNode:
    """Endpoint for updating a messages node"""

    exceptions_for_message_router_403(
        message_node=message_node, db=db, node_id=message_node_id
    )

    db_node = crud_message.update_message_node(
        db=db, node_id=message_node_id, new_node=message_node
    )

    exceptions_for_router_404(db_node=db_node, node_id=message_node_id)

    return db_node


@router.delete(
    "/message_nodes/{message_node_id}", response_model=schemas.MessageNode
)
def delete_message_node(node_id: int, db: CommonDB) -> models.MessageNode:
    """Endpoint for deleting a messages node"""

    db_node = crud_message.delete_message_node(db=db, node_id=node_id)

    exceptions_for_router_404(db_node=db_node, node_id=node_id)

    return db_node
