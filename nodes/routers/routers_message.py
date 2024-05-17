from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_message

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
        raise HTTPException(status_code=404, detail="Node not found")

    return db_message_node


@router.post("/message_nodes/", response_model=schemas.MessageNodeCreate)
def create_message_node_endpoint(
    message_node: schemas.MessageNodeCreate,
    db: CommonDB,
) -> models.MessageNode:

    parent_node = db.query(models.Node).get(message_node.parent_node_id)

    if not parent_node:
        raise HTTPException(
            status_code=404,
            detail=f"Parent node with id {message_node.parent_node_id} not found",
        )

    return crud_message.create_message_node(db=db, node=message_node)


@router.put(
    "/message_nodes/{message_node_id}",
    response_model=schemas.MessageNodeCreate,
)
def update_message_node_endpoint(
    node_id: int, node: schemas.MessageNodeCreate, db: CommonDB
):
    parent_node = db.query(models.Node).get(node.parent_node_id)

    if not parent_node:
        raise HTTPException(
            status_code=404,
            detail=f"Parent node with id {node.parent_node_id} not found",
        )

    db_node = crud_message.update_message_node(
        db=db, node_id=node_id, new_node=node
    )

    if db_node is None:
        raise HTTPException(
            status_code=404, detail=f"Node with id {node_id} not found"
        )

    return db_node


@router.delete(
    "/message_nodes/{message_node_id}", response_model=schemas.MessageNode
)
def delete_message_node(node_id: int, db: CommonDB):
    db_node = crud_message.delete_message_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node
