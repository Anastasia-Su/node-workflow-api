from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import or_, and_

from dependencies import CommonDB
from nodes import schemas, models
from nodes.models import NodeTypes


NodeTypeAlias = Union[
    schemas.MessageNodeCreate,
    schemas.StartNodeCreate,
    schemas.ConditionNodeCreate,
    schemas.EndNodeCreate,
]


def wrong_parent_exception(
    parent_node: NodeTypeAlias,
    node_type: NodeTypes,
    attribute: str,
) -> None:
    """Raise an exception when a parent node is of wrong type."""

    if parent_node and parent_node.node_type == node_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent {attribute} can't be of type {parent_node.node_type.upper()}",
        )


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


def different_workflow_exception(
    node: NodeTypeAlias, parent_node: NodeTypeAlias, parent_node_id: int
) -> None:
    """Raise an exception when a parent node is from different workflow"""

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


def exception_if_more_than_one_node(
    node: NodeTypeAlias,
    models_node: type(models.StartNode) | type(models.EndNode),
    db: CommonDB,
) -> None:
    """Raise an exception when specified workflow already has a node of this type"""

    existing_node = (
        db.query(models_node)
        .filter(
            models_node.workflow_id == node.workflow_id,
        )
        .first()
    )

    if existing_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This workflow already has {models_node().node_type.upper()} node",
        )
