from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_condition

router = APIRouter()


@router.get("/condition_nodes/", response_model=list[schemas.ConditionNode])
def read_condition_nodes(
    db: CommonDB,
) -> list[models.ConditionNode]:

    return crud_condition.get_condition_node_list(db=db)


@router.get(
    "/condition_nodes/{condition_node_id}/",
    response_model=schemas.ConditionNode,
)
def read_single_condition_node(
    condition_node_id: int, db: CommonDB
) -> models.ConditionNode:
    db_condition_node = crud_condition.get_condition_node_detail(
        db=db, node_id=condition_node_id
    )

    if db_condition_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_condition_node


@router.post("/condition_nodes/", response_model=schemas.ConditionNodeCreate)
def create_condition_node_endpoint(
    condition_node: schemas.ConditionNodeCreate,
    db: CommonDB,
) -> models.ConditionNode:

    # existing_node = crud.get_message_node_by_status_and_text(db=db, status=message_node.status, text=message_node.text)
    # if existing_node:
    #     raise HTTPException(status_code=400, detail="A node with the same status and text already exists")

    return crud_condition.create_condition_node(db=db, node=condition_node)


@router.put(
    "/condition_nodes/{condition_node_id}",
    response_model=schemas.ConditionNodeCreate,
)
def update_condition_node_endpoint(
    node_id: int, node: schemas.ConditionNodeCreate, db: CommonDB
):
    db_node = crud_condition.update_condition_node(
        db=db, node_id=node_id, new_condition=node.condition
    )
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete(
    "/condition_nodes/{condition_node_id}",
    response_model=schemas.ConditionNode,
)
def delete_condition_node(node_id: int, db: CommonDB):
    db_node = crud_condition.delete_condition_node(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node