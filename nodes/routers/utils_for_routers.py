from fastapi import HTTPException, status

from dependencies import CommonDB
from nodes import schemas, models
from nodes.models import NodeTypes


def exceptions_for_router_403(
    node: schemas.MessageNodeCreate | schemas.ConditionNodeCreate,
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
) -> None:
    """Raise exception if specified parent node not found or belongs to a different workflow"""

    if node.parent_node_id != 0 and not parent_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent node with id {node.parent_node_id} not found",
        )

    if parent_node:
        if (
            parent_node.workflow_id != 0
            and node.parent_node_id != 0
            and node.workflow_id != parent_node.workflow_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Parent node is from different workflow: {parent_node.workflow_id}.",
            )


def existing_message_exception(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
) -> None:
    """Raise exception if another message is already assigned to specified start node"""

    existing_message_node = (
        db.query(models.MessageNode)
        .filter(
            models.MessageNode.parent_node_id == message_node.parent_node_id,
            models.MessageNode.workflow_id == message_node.workflow_id,
        )
        .first()
    )

    if parent_node.node_type == NodeTypes.START and existing_message_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Another message node is already assigned to this start node.",
        )


def exceptions_for_condition_router_403(
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
):
    parent_node = db.query(models.Node).get(condition_node.parent_node_id)
    parent_message_node = db.query(models.Node).get(
        condition_node.parent_message_node_id
    )

    if not parent_message_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent message node with id {condition_node.parent_message_node_id} not found",
        )

    exceptions_for_router_403(node=condition_node, parent_node=parent_node)


def exceptions_for_message_router_403(
    message_node: schemas.MessageNodeCreate, db: CommonDB
) -> None:
    """Combine exceptions from the functions: exceptions_for_router_403, existing_message_exception"""

    parent_node = db.query(models.Node).get(message_node.parent_node_id)

    exceptions_for_router_403(node=message_node, parent_node=parent_node)

    existing_message_exception(
        message_node=message_node, db=db, parent_node=parent_node
    )


def exceptions_for_router_404(db_node, node_id) -> None:
    """Raise exception if the specified node is not found"""
    if db_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {node_id} not found",
        )
