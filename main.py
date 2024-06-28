from fastapi import FastAPI
from src.nodes.routers import (
    routers_message,
    routers_workflow,
    routers_condition,
    routers_condition_edge,
    routers_start,
    routers_end,
)

app = FastAPI()

app.include_router(routers_start.router)
app.include_router(routers_message.router)
app.include_router(routers_workflow.router)
app.include_router(routers_condition.router)
app.include_router(routers_condition_edge.router)
app.include_router(routers_end.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
