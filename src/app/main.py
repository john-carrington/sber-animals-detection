from fastapi import FastAPI
from src.app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "http://localhost:8000"
                   "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["Image Processing"])


@app.get("/")
def root():
    return {"message": "Welcome to the API!"}
