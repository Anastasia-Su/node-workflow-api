from fastapi import HTTPException, status

from dependencies import CommonDB
from nodes import schemas, models
from nodes.models import NodeTypes


def wrong_parent_exception(
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    node_type: NodeTypes,
    attribute: str,
) -> None:
    """Raise an exception when a parent node is of wrong type."""
    if parent_node and parent_node.node_type == node_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent {attribute} can't be of type {parent_node.node_type.upper()}",
        )


def existing_message_exception(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
) -> None:
    """Raise an exception if another message is already assigned to specified start node"""

    existing_message_node = (
        db.query(models.MessageNode)
        .filter(
            models.MessageNode.parent_node_id == message_node.parent_node_id,
            models.MessageNode.workflow_id == message_node.workflow_id,
        )
        .first()
    )

    if (
        parent_node
        and parent_node.node_type == NodeTypes.START
        and existing_message_node
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Another message node is already assigned to this start node.",
        )


def exceptions_for_router_403(
    node: schemas.MessageNodeCreate | schemas.ConditionNodeCreate,
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    parent_node_id: int,
) -> None:
    """Raise an exception if specified parent node not found or belongs to a different workflow"""

    if parent_node_id != 0 and not parent_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent node with id {parent_node_id} not found",
        )

    if parent_node:
        if (
            parent_node.workflow_id != 0
            and parent_node_id != 0
            and node.workflow_id != parent_node.workflow_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Parent {parent_node.node_type.upper()} node is from different workflow: {parent_node.workflow_id}.",
            )


def exceptions_for_condition_router_403(
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
) -> None:
    """Combine exceptions from the functions: exceptions_for_router_403, wrong_parent_exception"""

    parent_node = db.query(models.Node).get(condition_node.parent_node_id)
    parent_message_node = db.query(models.Node).get(
        condition_node.parent_message_node_id
    )

    exceptions = [
        (parent_node, NodeTypes.START, "node"),
        (parent_node, NodeTypes.END, "node"),
        (parent_message_node, NodeTypes.START, "message node"),
        (parent_message_node, NodeTypes.CONDITION, "message node"),
        (parent_message_node, NodeTypes.END, "message node"),
    ]

    for parent_node, node_type, attribute in exceptions:
        wrong_parent_exception(
            parent_node=parent_node, node_type=node_type, attribute=attribute
        )

    exceptions_for_router_403(
        node=condition_node,
        parent_node=parent_node,
        parent_node_id=condition_node.parent_node_id,
    )

    exceptions_for_router_403(
        node=condition_node,
        parent_node=parent_message_node,
        parent_node_id=condition_node.parent_message_node_id,
    )


def exceptions_for_message_router_403(
    message_node: schemas.MessageNodeCreate, db: CommonDB
) -> None:
    """Combine exceptions from the functions: exceptions_for_router_403, existing_message_exception"""

    parent_node = db.query(models.Node).get(message_node.parent_node_id)

    exceptions_for_router_403(
        node=message_node,
        parent_node=parent_node,
        parent_node_id=message_node.parent_node_id,
    )

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
