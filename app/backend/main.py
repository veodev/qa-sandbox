from api.router import api_router
from fastapi import FastAPI

app = FastAPI(title="QA Sandbox API")
app.include_router(api_router, prefix="/api")
