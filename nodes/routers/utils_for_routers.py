from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import or_, and_

from dependencies import CommonDB
from nodes import schemas, models
from nodes.models import NodeTypes

import logging

logger = logging.getLogger(__name__)


NodeTypeAlias = Union[
    schemas.MessageNodeCreate,
    schemas.StartNodeCreate,
    schemas.ConditionNodeCreate,
    schemas.EndNodeCreate,
]


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


#
# def existing_message_exception(
#     message_node: schemas.MessageNodeCreate,
#     db: CommonDB,
#     parent_node: (
#         schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
#     ),
# ) -> None:
#     """Raise an exception if another message is already assigned to specified start node"""
#
#     existing_message_node = (
#         db.query(models.MessageNode)
#         .filter(
#             models.MessageNode.parent_node_id == message_node.parent_node_id,
#             models.MessageNode.workflow_id == message_node.workflow_id,
#         )
#         .first()
#     )
#
#     if (
#         parent_node
#         and parent_node.node_type == NodeTypes.START
#         and existing_message_node
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Another message node is already assigned to this start node.",
#         )


def existing_child_exception(
    node: (
        schemas.MessageNodeCreate
        | schemas.ConditionNodeCreate
        | schemas.EndNodeCreate
    ),
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    db: CommonDB,
    node_id: int | None = None,
) -> None:
    """Raise an exception if parent message node already has a child node"""

    exception_models = [
        models.MessageNode,
        models.ConditionNode,
        models.EndNode,
    ]

    if parent_node:
        for exception_model in exception_models:
            existing_message_child = (
                db.query(exception_model)
                .filter(
                    and_(
                        exception_model.parent_node_id == node.parent_node_id,
                        exception_model.workflow_id == node.workflow_id,
                        or_(
                            parent_node.node_type == NodeTypes.MESSAGE,
                            parent_node.node_type == NodeTypes.START,
                        ),
                    )
                )
                .first()
            )

            if (
                existing_message_child
                and node.parent_node_id != 0
                and existing_message_child.id != node_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Parent node with id {node.parent_node_id} already has a child node with id "
                    f"{existing_message_child.id}.",
                )


def workflow_not_found_exception(
    node: NodeTypeAlias,
    db: CommonDB,
) -> None:
    """Raise an exception if specified workflow not found"""

    existing_workflow = (
        db.query(models.Workflow)
        .filter(
            models.Workflow.id == node.workflow_id,
        )
        .first()
    )

    if node.workflow_id != 0 and not existing_workflow:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Workflow with id {node.workflow_id} not found.",
        )


def exception_for_wrong_ref_id(
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    parent_node_id: int,
) -> None:
    """Raise an exception when a parent or reference node not found."""

    if parent_node_id != 0 and parent_node is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent node with id {parent_node_id} not found",
        )


def exceptions_for_router_403(
    node: (
        schemas.MessageNodeCreate
        | schemas.ConditionNodeCreate
        | schemas.EndNodeCreate
    ),
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    parent_node_id: int,
    db: CommonDB,
) -> None:
    """Raise an exception if
    specified parent node not found or belongs to a different workflow,
    or if specified workflow not found
    or if parent_node is a Message node with existing child node"""

    workflow_not_found_exception(node=node, db=db)

    exception_for_wrong_ref_id(
        parent_node=parent_node, parent_node_id=parent_node_id
    )

    if parent_node:
        if (
            parent_node.workflow_id != 0
            and node.workflow_id != 0
            and parent_node_id != 0
            and node.workflow_id != parent_node.workflow_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Parent {parent_node.node_type.upper()} node "
                f"is from different workflow: {parent_node.workflow_id}.",
            )


def exceptions_for_condition_router_403(
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
    node_id: int | None = None,
) -> None:
    """Combine exceptions from the functions:
    exceptions_for_router_403,
    wrong_parent_exception,
    existing_child_exception,"""

    parent_node = db.query(models.Node).get(condition_node.parent_node_id)
    parent_message_node = db.query(models.Node).get(
        condition_node.parent_message_node_id
    )

    exceptions_nodes = [
        (NodeTypes.START, "node"),
        (NodeTypes.END, "node"),
    ]

    exceptions_message_nodes = [
        (NodeTypes.START, "message node"),
        (NodeTypes.CONDITION, "message node"),
        (NodeTypes.END, "message node"),
    ]
    for node_type, attribute in exceptions_nodes:
        wrong_parent_exception(
            parent_node=parent_node, node_type=node_type, attribute=attribute
        )

    for node_type, attribute in exceptions_message_nodes:
        wrong_parent_exception(
            parent_node=parent_message_node,
            node_type=node_type,
            attribute=attribute,
        )

    exceptions_for_router_403(
        node=condition_node,
        parent_node=parent_node,
        parent_node_id=condition_node.parent_node_id,
        db=db,
    )
    exceptions_for_router_403(
        node=condition_node,
        parent_node=parent_message_node,
        parent_node_id=condition_node.parent_message_node_id,
        db=db,
    )

    existing_child_exception(
        node_id=node_id,
        node=condition_node,
        parent_node=parent_node,
        db=db,
    )


def exceptions_for_condition_edge_router_403(
    edge: schemas.ConditionEdgeCreate, db: CommonDB
) -> None:
    """Raise an exception if specified edge already exists
    or reference condition does not exist"""

    reference_node = db.query(models.Node).get(edge.condition_node_id)

    exception_for_wrong_ref_id(
        parent_node=reference_node, parent_node_id=edge.condition_node_id
    )

    existing_edge = (
        db.query(models.ConditionEdge)
        .filter(
            models.ConditionEdge.condition_node_id == edge.condition_node_id,
            models.ConditionEdge.edge == edge.edge,
        )
        .first()
    )

    if existing_edge and edge.condition_node_id != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Edge with these data already exists.",
        )


def exceptions_for_message_router_403(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
    node_id: int | None = None,
) -> None:
    """Combine exceptions from the functions:
    exceptions_for_router_403,
    wrong_parent_exception,
    existing_child_exception"""

    parent_node = db.query(models.Node).get(message_node.parent_node_id)

    wrong_parent_exception(
        parent_node=parent_node, node_type=NodeTypes.END, attribute="node"
    )

    exceptions_for_router_403(
        node=message_node,
        parent_node=parent_node,
        parent_node_id=message_node.parent_node_id,
        db=db,
    )

    existing_child_exception(
        node=message_node, parent_node=parent_node, db=db, node_id=node_id
    )


def exceptions_for_end_router_403(
    end_node: schemas.EndNodeCreate,
    db: CommonDB,
) -> None:
    """Combine exceptions from the functions:
    exceptions_for_router_403,
    wrong_parent_exception"""

    parent_node = db.query(models.Node).get(end_node.parent_node_id)

    exceptions = [NodeTypes.START, NodeTypes.END, NodeTypes.CONDITION]

    for node_type in exceptions:
        wrong_parent_exception(
            parent_node=parent_node, node_type=node_type, attribute="node"
        )

    existing_child_exception(
        node=end_node,
        parent_node=parent_node,
        db=db,
    )

    exceptions_for_router_403(
        node=end_node,
        parent_node=parent_node,
        parent_node_id=end_node.parent_node_id,
        db=db,
    )


def exceptions_for_router_404(db_node, node_id) -> None:
    """Raise exception if the specified node is not found"""

    if db_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {node_id} not found",
        )
