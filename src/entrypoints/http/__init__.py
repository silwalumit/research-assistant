from fastapi import FastAPI

from src.entrypoints.http.agent.routes import router


def register_routes(app: FastAPI):
    app.include_router(router)
