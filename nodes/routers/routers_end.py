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

    if (
        not db.query(models.MessageNode)
        .filter(models.MessageNode.id == end_node.message_node_id)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Message node not found")

    return crud_end.create_end_node(db=db, node=end_node)


@router.put(
    "/end_nodes/{end_node_id}",
    response_model=schemas.EndNodeCreate,
)
def update_end_node_endpoint(
    node_id: int, node: schemas.EndNodeCreate, db: CommonDB
):
    db_node = crud_end.update_end_node(
        db=db,
        node_id=node_id,
        new_message=node.message,
        new_message_node_id=node.message_node_id,
    )

    if (
        not db.query(models.MessageNode)
        .filter(models.MessageNode.id == node.message_node_id)
        .first()
    ):
        raise HTTPException(status_code=404, detail="Message node not found")

    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete("/end_nodes/{end_node_id}", response_model=schemas.EndNode)
def delete_end_node(node_id: int, db: CommonDB):
    db_node = crud_end.delete_end_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node
