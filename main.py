from fastapi import FastAPI
from nodes.routers import routers_nodes, routers_message

app = FastAPI()

app.include_router(routers_message.router)
app.include_router(routers_nodes.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
