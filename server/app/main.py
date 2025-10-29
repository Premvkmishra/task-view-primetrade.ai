import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers.auth import router as auth_router
from .api.routers.tasks import router as tasks_router

app = FastAPI(title="Secure API", version="1.0.0", openapi_url="/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"success": True, "data": {"status": "ok"}, "message": "Healthy"}

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"]) 
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"]) 
