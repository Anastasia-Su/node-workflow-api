from fastapi import FastAPI
from nodes import routers

app = FastAPI()

app.include_router(routers.router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
