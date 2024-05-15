from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_message

router = APIRouter()


# def get_db() -> Session:
#     db = SessionLocal()
#
#     try:
#         yield db
#     finally:
#         db.close()


@router.get("/")
def root() -> dict:
    print("Received request at root endpoint")

    return {"message": "Hello World"}


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

    # existing_node = crud.get_message_node_by_status_and_text(db=db, status=message_node.status, text=message_node.text)
    # if existing_node:
    #     raise HTTPException(status_code=400, detail="A node with the same status and text already exists")

    return crud_message.create_message_node(db=db, node=message_node)


@router.put(
    "/message_nodes/{message_node_id}",
    response_model=schemas.MessageNodeCreate,
)
def update_message_node_endpoint(
    node_id: int, node: schemas.MessageNodeCreate, db: CommonDB
):
    db_node = crud_message.update_message_node(
        db=db, node_id=node_id, new_status=node.status, new_text=node.text
    )
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete(
    "/message_nodes/{message_node_id}", response_model=schemas.MessageNode
)
def delete_message_node(node_id: int, db: CommonDB):
    db_node = crud_message.delete_message_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node
