import networkx as nx

from utils.utils import execute_workflow


from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_workflow

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
def read_single_workflow(workflow_id: int, db: CommonDB) -> schemas.Workflow:
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
        db=db, node_id=node_id, new_node=node
    )

    if db_node is None:
        raise HTTPException(
            status_code=404, detail=f"Workflow with id {node_id} not found"
        )

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


@router.post("/workflows/execute")
def run_workflow(db: CommonDB, workflow_id: int):
    db_workflow_node = crud_workflow.get_workflow_detail(
        db=db, node_id=workflow_id
    )

    try:
        result = execute_workflow(db, workflow_id)
        response = {
            "message": "Workflow executed successfully",
            "execution_time": result["execution_time"],
            "graph": nx.node_link_data(result["graph"]),
        }
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
