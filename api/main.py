from fastapi import FastAPI
from api.routers import inference

app = FastAPI(
    title="Failure-Aware GenAI System",
    version="1.0"
)

app.include_router(inference.router)
