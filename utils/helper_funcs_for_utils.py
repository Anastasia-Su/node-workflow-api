from fastapi import HTTPException, status


def exception_no_next_node(current_node):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No associated node found for current node with id {current_node.id}",
    )


def exception_no_start_node():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Start node not found",
    )


def exception_unknown_node_type(current_node):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Unknown node type: {type(current_node)}",
    )


def find_next_node(node_list, current_node):

    return next(
        (node for node in node_list if node.parent_node_id == current_node.id),
        None,
    )
