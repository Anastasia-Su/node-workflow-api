from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_start

router = APIRouter()


@router.get("/start_nodes/", response_model=list[schemas.StartNode])
def read_start_nodes(
    db: CommonDB,
) -> list[models.StartNode]:

    return crud_start.get_start_node_list(db=db)


@router.get("/start_nodes/{start_node_id}/", response_model=schemas.StartNode)
def read_single_start_node(
    start_node_id: int, db: CommonDB
) -> models.StartNode:
    db_start_node = crud_start.get_start_node_detail(
        db=db, node_id=start_node_id
    )

    if db_start_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_start_node


@router.post("/start_nodes/", response_model=schemas.StartNodeCreate)
def create_start_node_endpoint(
    start_node: schemas.StartNodeCreate,
    db: CommonDB,
) -> models.StartNode:

    return crud_start.create_start_node(db=db, node=start_node)


@router.put(
    "/start_nodes/{start_node_id}",
    response_model=schemas.StartNodeCreate,
)
def update_start_node_endpoint(
    node_id: int, node: schemas.StartNodeCreate, db: CommonDB
):
    db_node = crud_start.update_start_node(
        db=db,
        node_id=node_id,
        new_node=node,
    )

    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete(
    "/start_nodes/{start_node_id}", response_model=schemas.StartNode
)
def delete_start_node(node_id: int, db: CommonDB):
    db_node = crud_start.delete_start_node(db=db, node_id=node_id)

    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node
