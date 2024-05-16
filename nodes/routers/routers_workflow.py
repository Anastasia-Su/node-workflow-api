from nodes.utils import execute_workflow


from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_workflow


router = APIRouter()


@router.get("/workflow_nodes/", response_model=list[schemas.WorkflowNode])
def read_workflow_nodes(
    db: CommonDB,
) -> list[models.WorkflowNode]:

    return crud_workflow.get_workflow_list(db=db)


@router.get(
    "/workflows/{workflow_id}/",
    response_model=schemas.WorkflowNode,
)
def read_single_workflow(
    workflow_id: int, db: CommonDB
) -> models.WorkflowNode:
    db_workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )

    if db_workflow_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_workflow_node


@router.post("/workflows/", response_model=schemas.WorkflowNodeCreate)
def create_workflow_endpoint(
    workflow: schemas.WorkflowNodeCreate,
    db: CommonDB,
) -> models.WorkflowNode:

    # existing_node = crud.get_message_node_by_status_and_text(db=db, status=message_node.status, text=message_node.text)
    # if existing_node:
    #     raise HTTPException(status_code=400, detail="A node with the same status and text already exists")

    return crud_workflow.create_workflow(db=db, node=workflow)


@router.put(
    "/workflow_nodes/{workflow_node_id}",
    response_model=schemas.WorkflowNodeCreate,
)
def update_workflow_node_endpoint(
    node_id: int, node: schemas.WorkflowNodeCreate, db: CommonDB
):
    db_node = crud_workflow.update_workflow(
        db=db,
        node_id=node_id,
        new_start_node=node.start_node,
        new_message_node=node.message_node,
        new_condition_node=node.condition_node,
        new_end_node=node.end_node,
    )
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@router.delete(
    "/workflow_nodes/{workflow_node_id}",
    response_model=schemas.WorkflowNode,
)
def delete_workflow_node(node_id: int, db: CommonDB):
    db_node = crud_workflow.delete_workflow(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


#
# @router.post("/workflow/construct/")
# def construct_workflow(
#     message_ids: list[int], condition_ids: list[int], db: CommonDB
# ):
#     # Fetch messages and conditions based on the provided IDs
#     messages = get_messages_from_database(db, message_ids)
#     conditions = get_conditions_from_database(db, condition_ids)
#
#     # Create a start node
#     start_node = WorkFlowNodeCreate(
#         status=MessageStatus.PENDING, text="Start of workflow"
#     )
#     db_node = create_workflow_node(db, start_node)
#
#     # Create message nodes
#     for message_id in message_ids:
#         message = get_message_from_database(db, message_id)
#         message_node = WorkFlowNodeCreate(
#             status=message.status, text=message.text
#         )
#         db_node = create_workflow_node(db, message_node)
#         db_node.start_node_id = start_node.id
#
#     # Create condition nodes
#     for condition_id in condition_ids:
#         condition = get_condition_from_database(db, condition_id)
#         condition_node = WorkFlowNodeCreate(
#             status=MessageStatus.PENDING, text=condition.condition
#         )
#         db_node = create_workflow_node(db, condition_node)
#         db_node.start_node_id = start_node.id

# Link nodes together based on your workflow logic
# You would need to implement this logic based on your requirements

# return {"message": "Workflow constructed successfully"}

#
# @router.post("/workflow/run/")
# def run_workflow(start_node_id: int, db: Session = Depends(get_db)):
#     # Retrieve the start node from the database
#     start_node = get_workflow_node(db, start_node_id)
#
#     # Run the workflow
#     run_workflow_logic(start_node)
#
#     return {"message": "Workflow executed successfully"}
#


# @router.post("/workflow/execute")
# def execute_workflow(db: CommonDB):
#     start_node = crud_nodes.get_start_node(db=db)
#     if not start_node:
#         raise HTTPException(status_code=404, detail="Start node not found")
#
#     try:
#         execute_workflow(start_node)
#         return {"message": "Workflow executed successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
