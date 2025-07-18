from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # bootstrap settings
    app.state.settings = Settings()
    yield


# Initialize FastAPI app
app = FastAPI(
    title="Research Assistant Agent",
    description="A mini Research Assistant agent that answers natural-language questions about local documents",
    version="1.0.0",
    lifespan=lifespan,
)
