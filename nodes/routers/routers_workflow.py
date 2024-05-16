from nodes.utils import execute_workflow

from fastapi import HTTPException, APIRouter

from dependencies import CommonDB
from nodes.crud import crud_nodes

router = APIRouter()


@router.post("/workflow/execute")
def execute_workflow(db: CommonDB):
    start_node = crud_nodes.get_start_node(db=db)
    if not start_node:
        raise HTTPException(status_code=404, detail="Start node not found")

    try:
        execute_workflow(start_node)
        return {"message": "Workflow executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
