from fastapi import HTTPException, APIRouter, status

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_message
from nodes.models import NodeTypes

router = APIRouter()


@router.get("/message_nodes/", response_model=list[schemas.MessageNode])
def read_message_nodes(
    db: CommonDB,
) -> list[models.MessageNode]:

    return crud_message.get_message_node_list(db=db)


@router.get(
    "/message_nodes/{message_node_id}/", response_model=schemas.MessageNode
)
def read_single_message_node(
    message_node_id: int, db: CommonDB
) -> models.MessageNode:
    db_message_node = crud_message.get_message_node_detail(
        db=db, node_id=message_node_id
    )

    if db_message_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {message_node_id} not found",
        )

    return db_message_node


@router.post("/message_nodes/", response_model=schemas.MessageNodeCreate)
def create_message_node_endpoint(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
) -> models.MessageNode:

    parent_node = db.query(models.Node).get(message_node.parent_node_id)
    message_node_list = crud_message.get_message_node_list(db=db)

    existing_message_node = next(
        (
            existing_message
            for existing_message in message_node_list
            if existing_message.parent_node_id == message_node.parent_node_id
            and message_node.workflow_id == existing_message.workflow_id
        ),
        None,
    )
    if parent_node:
        if (
            parent_node.workflow_id != 0
            and message_node.parent_node_id != 0
            and message_node.workflow_id != parent_node.workflow_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Parent node is from different workflow: {parent_node.workflow_id}.",
            )

        if parent_node.node_type == NodeTypes.START and existing_message_node:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Another message node is already assigned to this start node.",
            )

    if message_node.parent_node_id != 0 and not parent_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent node with id {message_node.parent_node_id} not found",
        )

    return crud_message.create_message_node(db=db, node=message_node)


@router.put(
    "/message_nodes/{message_node_id}",
    response_model=schemas.MessageNodeCreate,
)
def update_message_node_endpoint(
    message_node_id: int, message_node: schemas.MessageNodeCreate, db: CommonDB
):
    parent_node = db.query(models.Node).get(message_node.parent_node_id)

    existing_message_node = (
        db.query(models.MessageNode)
        .filter(
            models.MessageNode.parent_node_id == message_node.parent_node_id,
            models.MessageNode.workflow_id == message_node.workflow_id,
        )
        .first()
    )

    if message_node.parent_node_id != 0 and not parent_node:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Parent node with id {message_node.parent_node_id} not found",
        )

    if parent_node:
        if (
            parent_node.workflow_id != 0
            and message_node.parent_node_id != 0
            and message_node.workflow_id != parent_node.workflow_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Parent node is from different workflow: {parent_node.workflow_id}.",
            )

        if parent_node.node_type == NodeTypes.START and existing_message_node:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Another message node is already assigned to this start node.",
            )

    db_node = crud_message.update_message_node(
        db=db, node_id=message_node_id, new_node=message_node
    )

    if db_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {message_node_id} not found",
        )

    return db_node


#
# @router.put(
#     "/message_nodes/{message_node_id}",
#     response_model=schemas.MessageNodeCreate,
# )
# def update_message_node_endpoint(
#     message_node_id: int, node: schemas.MessageNodeCreate, db: CommonDB
# ):
#     parent_node = db.query(models.Node).get(node.parent_node_id)
#     message_node = crud_message.get_message_node_detail(
#         db=db, node_id=message_node_id
#     )
#
#     if parent_node:
#         if (
#             parent_node.workflow_id != 0
#             and node.parent_node_id != 0
#             and node.workflow_id != parent_node.workflow_id
#         ):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Parent node is from different workflow: {parent_node.workflow_id}.",
#             )
#
#         if parent_node.node_type == NodeTypes.START:
#             existing_message_node = (
#                 db.query(models.MessageNode)
#                 .filter(
#                     models.MessageNode.parent_node_id == node.parent_node_id,
#                     models.MessageNode.workflow_id == node.workflow_id,
#                 )
#                 .first()
#             )
#             if existing_message_node:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Another message node is already assigned to this start node.",
#                 )
#
#     if node.parent_node_id != 0 and not parent_node:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Parent node with id {node.parent_node_id} not found",
#         )
#
#     db_node = crud_message.update_message_node(
#         db=db, node_id=message_node_id, new_node=node
#     )
#
#     if db_node is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Node with id {message_node_id} not found",
#         )
#
#     return db_node
#


@router.delete(
    "/message_nodes/{message_node_id}", response_model=schemas.MessageNode
)
def delete_message_node(node_id: int, db: CommonDB):
    db_node = crud_message.delete_message_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with id {node_id} not found",
        )

    return db_node
