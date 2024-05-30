from typing import Union
from fastapi import HTTPException, status

from dependencies import CommonDB
from nodes import schemas, models
from nodes.models import NodeTypes
from nodes.routers.exceptions_for_routers.building_blocks import (
    workflow_not_found_exception,
    exception_for_wrong_ref_id,
    different_workflow_exception,
    wrong_parent_exception,
    existing_child_exception,
    exception_if_more_than_one_node,
    existing_two_children_exception,
)


NodeTypeAlias = Union[
    schemas.MessageNodeCreate,
    schemas.StartNodeCreate,
    schemas.ConditionNodeCreate,
    schemas.EndNodeCreate,
]

NodeTypeCreatedAlias = Union[
    schemas.MessageNode,
    schemas.StartNode,
    schemas.ConditionNode,
    schemas.EndNode,
]


def exceptions_for_router_403(
    node: NodeTypeAlias,
    parent_node: (
        schemas.MessageNode | schemas.StartNode | schemas.ConditionNode
    ),
    parent_node_id: int,
    db: CommonDB,
) -> None:
    """Raise an exception if
    specified parent node not found or belongs to a different workflow,
    or if specified workflow not found"""

    workflow_not_found_exception(node=node, db=db)

    exception_for_wrong_ref_id(
        parent_node=parent_node, parent_node_id=parent_node_id
    )

    different_workflow_exception(
        node=node, parent_node=parent_node, parent_node_id=parent_node_id
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

    parent_node = db.get(models.Node, condition_node.parent_node_id)
    parent_message_node = db.get(
        models.Node, condition_node.parent_message_node_id
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

    existing_two_children_exception(
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

    reference_node = db.get(models.Node, edge.condition_node_id)

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

    parent_node = db.get(models.Node, message_node.parent_node_id)

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

    existing_two_children_exception(
        node_id=node_id,
        node=message_node,
        parent_node=parent_node,
        db=db,
    )


def exceptions_for_end_router_403(
    end_node: schemas.EndNodeCreate,
    db: CommonDB,
) -> None:
    """Combine exceptions from the functions:
    exceptions_for_router_403,
    wrong_parent_exception"""

    parent_node = db.get(models.Node, end_node.parent_node_id)

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


def exceptions_for_start_router_403(
    start_node: schemas.StartNodeCreate, db: CommonDB
) -> None:
    """Combine exceptions from the functions:
    workflow_not_found_exception,
    exception_if_more_than_one_node,"""

    workflow_not_found_exception(node=start_node, db=db)
    exception_if_more_than_one_node(
        node=start_node, models_node=models.StartNode, db=db
    )


def exceptions_for_router_404(
    db_node: NodeTypeCreatedAlias, node_id: int
) -> None:
    """Raise exception if the specified node is not found"""

    if db_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {node_id} not found",
        )
