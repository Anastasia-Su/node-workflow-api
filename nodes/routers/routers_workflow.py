import networkx as nx

from nodes.routers.utils_for_routers import exceptions_for_router_404

# from utils.utils_for_execute_router import execute_workflow

from utils.execute_workflow_main import execute_workflow

# from utils.utils_alternative import execute_workflow


from fastapi import HTTPException, APIRouter, status
from fastapi.responses import JSONResponse

from dependencies import CommonDB
from nodes import models, schemas
from nodes.crud import crud_workflow

router = APIRouter()


@router.get("/workflows/", response_model=list[schemas.Workflow])
def read_workflows(
    db: CommonDB,
) -> list[models.Workflow]:
    """Endpoint for retrieving all workflows"""

    return crud_workflow.get_workflow_list(db=db)


@router.get(
    "/workflows/{workflow_id}/",
    response_model=schemas.Workflow,
)
def read_single_workflow(workflow_id: int, db: CommonDB) -> schemas.Workflow:
    """Endpoint for retrieving a single workflow"""

    db_workflow = crud_workflow.get_workflow_detail(db=db, node_id=workflow_id)
    exceptions_for_router_404(db_node=db_workflow, node_id=workflow_id)

    return db_workflow


@router.post("/workflows/", response_model=schemas.WorkflowCreate)
def create_workflow_endpoint(
    workflow: schemas.WorkflowCreate,
    db: CommonDB,
) -> models.Workflow:
    """Endpoint for creating a workflow"""

    return crud_workflow.create_workflow(db=db, node=workflow)


@router.put(
    "/workflows/{workflow_id}",
    response_model=schemas.WorkflowCreate,
)
def update_workflow_endpoint(
    workflow_id: int, workflow: schemas.WorkflowCreate, db: CommonDB
) -> models.Workflow:
    """Endpoint for updating a workflow"""

    db_workflow = crud_workflow.update_workflow(
        db=db, node_id=workflow_id, new_node=workflow
    )

    exceptions_for_router_404(db_node=db_workflow, node_id=workflow_id)

    return db_workflow


@router.delete(
    "/workflows/{workflow_id}",
    response_model=schemas.Workflow,
)
def delete_workflow(workflow_id: int, db: CommonDB) -> models.Workflow:
    """Endpoint for deleting a workflow"""

    db_workflow = crud_workflow.delete_workflow(db=db, node_id=workflow_id)

    exceptions_for_router_404(db_node=db_workflow, node_id=workflow_id)

    return db_workflow


@router.post("/workflows/execute")
def run_workflow(db: CommonDB, workflow_id: int) -> JSONResponse:
    """Endpoint for executing a workflow"""

    db_workflow = crud_workflow.get_workflow_detail(db=db, node_id=workflow_id)
    exceptions_for_router_404(db_node=db_workflow, node_id=workflow_id)

    try:
        result = execute_workflow(db, workflow_id)
        response = {
            "message": "Workflow executed successfully",
            "execution_time": result["execution_time"],
            "graph": nx.node_link_data(result["graph"]),
        }
        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
