from fastapi import FastAPI
from src.app.api.endpoints import router

app = FastAPI()

app.include_router(router, prefix="/api", tags=["Image Processing"])


@app.get("/")
def root():
    return {"message": "Welcome to the API!"}
