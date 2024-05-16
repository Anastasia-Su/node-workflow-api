from fastapi import FastAPI
from nodes.routers import routers_message, routers_workflow, routers_condition

app = FastAPI()

app.include_router(routers_message.router)
app.include_router(routers_workflow.router)
app.include_router(routers_condition.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
