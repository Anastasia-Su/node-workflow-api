from nodes.utils import execute_workflow


from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes import models, schemas, crud
from nodes.crud import crud_workflow, crud_message, crud_condition

router = APIRouter()


@router.get("/workflows/", response_model=list[schemas.Workflow])
def read_workflows(
    db: CommonDB,
) -> list[models.Workflow]:

    return crud_workflow.get_workflow_list(db=db)


@router.get(
    "/workflows/{workflow_id}/",
    response_model=schemas.Workflow,
)
def read_single_workflow(workflow_id: int, db: CommonDB) -> models.Workflow:
    db_workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )

    if db_workflow_node is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return db_workflow_node


@router.post("/workflows/", response_model=schemas.WorkflowCreate)
def create_workflow_endpoint(
    workflow: schemas.WorkflowCreate,
    db: CommonDB,
) -> models.Workflow:

    return crud_workflow.create_workflow(db=db, node=workflow)


@router.put(
    "/workflows/{workflow_id}",
    response_model=schemas.WorkflowCreate,
)
def update_workflow_endpoint(
    node_id: int, node: schemas.WorkflowCreate, db: CommonDB
):
    db_node = crud_workflow.update_workflow(
        db=db,
        node_id=node_id,
        new_start_node=node.start_node,
        new_message_nodes=node.message_nodes,
        new_condition_nodes=node.condition_nodes,
        new_end_node=node.end_node,
    )
    if db_node is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return db_node


@router.delete(
    "/workflows/{workflow_id}",
    response_model=schemas.Workflow,
)
def delete_workflow(node_id: int, db: CommonDB):
    db_node = crud_workflow.delete_workflow(db=db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return db_node


#
# #
# @router.post("/workflows/{workflow_id}/construct")
# def construct_workflow(db: CommonDB, workflow_id: int):
#     workflow_node = crud_workflow.get_workflow_detail(
#         db=db, node_id=workflow_id
#     )
#     start_node = workflow_node.start_node
#     messages = workflow_node.message_nodes
#     conditions = workflow_node.condition_nodes
#     end_node = workflow_node.end_node
#
#     db_node = start_node
#
#     for message in messages:
#         message = crud_message.get_message_node_detail(
#             db=db, node_id=message.id
#         )
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
#
#
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

#
# @router.post("/workflows/{workflow_id}/execute")
# def execute_workflow(db: CommonDB, workflow_id: int):
#     db_workflow_node = crud_workflow.get_workflow_detail(
#         db=db, node_id=workflow_id
#     )
#     start_node = db_workflow_node.start_node
#     if not start_node:
#         raise HTTPException(status_code=404, detail="Start node not found")
#
#     try:
#         execute_workflow(start_node)
#         return {"message": "Workflow executed successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
