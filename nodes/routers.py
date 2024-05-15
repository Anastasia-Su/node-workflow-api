from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import SessionLocal
from nodes import models, schemas, crud

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root() -> dict:
    print("Received request at root endpoint")
    return {"message": "Hello World"}


@router.get("/message_nodes/", response_model=list[schemas.MessageNode])
def read_message_nodes(
    db: Session = Depends(get_db),
) -> list[models.MessageNode]:
    return crud.get_message_node_list(db=db)


@router.get(
    "/message_nodes/{message_node_id}/", response_model=schemas.MessageNode
)
def read_single_message_node(
    message_node_id: int, db: Session = Depends(get_db)
) -> models.MessageNode:
    db_message_node = crud.get_message_node_detail(
        db=db, node_id=message_node_id
    )

    if db_message_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_message_node


@router.post("/message_nodes/", response_model=schemas.MessageNodeCreate)
def create_message_node_endpoint(
    message_node: schemas.MessageNodeCreate,
    db: Session = Depends(get_db),
) -> models.MessageNode:
    node = crud.get_message_node_detail(db=db, node_id=message_node.id)

    if node:
        raise HTTPException(status_code=400, detail="This node already exists")

    return crud.create_message_node(db=db, node=message_node)
