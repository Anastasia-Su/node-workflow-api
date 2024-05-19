from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_end

router = APIRouter()


@router.get("/end_nodes/", response_model=list[schemas.EndNode])
def read_end_nodes(
    db: CommonDB,
) -> list[models.EndNode]:

    return crud_end.get_end_node_list(db=db)


@router.get("/end_nodes/{end_node_id}/", response_model=schemas.EndNode)
def read_single_end_node(end_node_id: int, db: CommonDB) -> models.EndNode:
    db_end_node = crud_end.get_end_node_detail(db=db, node_id=end_node_id)

    if db_end_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_end_node


@router.post("/end_nodes/", response_model=schemas.EndNodeCreate)
def create_end_node_endpoint(
    end_node: schemas.EndNodeCreate,
    db: CommonDB,
) -> models.EndNode:

    parent_message_node = db.query(models.Node).get(end_node.parent_node_id)

    if not parent_message_node:
        raise HTTPException(
            status_code=404,
            detail=f"Parent message node with id {end_node.parent_node_id} not found",
        )

    return crud_end.create_end_node(db=db, node=end_node)


@router.put(
    "/end_nodes/{end_node_id}",
    response_model=schemas.EndNodeCreate,
)
def update_end_node_endpoint(
    node_id: int, node: schemas.EndNodeCreate, db: CommonDB
):
    parent_message_node = db.query(models.Node).get(node.parent_node_id)

    if not parent_message_node:
        raise HTTPException(
            status_code=404,
            detail=f"Parent message node with id {node.parent_node_id} not found",
        )

    db_node = crud_end.update_end_node(
        db=db,
        node_id=node_id,
        new_node=node,
    )

    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete("/end_nodes/{end_node_id}", response_model=schemas.EndNode)
def delete_end_node(node_id: int, db: CommonDB):
    db_node = crud_end.delete_end_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node
