from typing import Union, Any

from fastapi import HTTPException, status

from nodes import models


NodeTypeAlias = Union[
    models.MessageNode,
    models.ConditionNode,
    models.StartNode,
    models.EndNode,
]


def exception_no_next_node(current_node: NodeTypeAlias) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No associated node found for current node with id {current_node.id}",
    )


def exception_no_start_node() -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Start node not found",
    )


def exception_unknown_node_type(current_node: NodeTypeAlias) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Unknown node type: {type(current_node)}",
    )


def exception_for_infinite_loop(
    iteration_count: int, num_of_iterations: int
) -> None:

    if iteration_count >= num_of_iterations:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Reached maximum iterations: {num_of_iterations}, possible infinite loop detected",
        )


def find_next_node(
    node_list: list[NodeTypeAlias], current_node: NodeTypeAlias
) -> NodeTypeAlias:

    return next(
        (node for node in node_list if node.parent_node_id == current_node.id),
        None,
    )


def get_node_lists(workflow_node: models.Workflow, workflow_id: int) -> tuple[
    models.StartNode,
    list[models.MessageNode],
    list[models.ConditionNode],
    list[models.EndNode],
]:

    start_node = (
        workflow_node.start_node
        if workflow_node.start_node
        and workflow_node.start_node.id == workflow_id
        else None
    )
    if not start_node:
        exception_no_start_node()

    message_nodes = [
        node
        for node in workflow_node.message_nodes
        if node.workflow_id == workflow_id
    ]
    condition_nodes = [
        node
        for node in workflow_node.condition_nodes
        if node.workflow_id == workflow_id
    ]
    end_nodes = [
        node
        for node in workflow_node.end_nodes
        if node.workflow_id == workflow_id
    ]

    return start_node, message_nodes, condition_nodes, end_nodes
