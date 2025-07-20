from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config.settings import Settings
from src.shared.logging.logger import setup_logger

settings = Settings()
setup_logger(settings.log)


logger = getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    from src.app.agent import ResearchAgent

    logger.info("Starting application")
    # bootstrap settings
    logger.debug("Bootstraping app settings")
    app.state.settings = settings

    logger.debug("Bootstrap Agent")
    agent = ResearchAgent(settings=settings)
    app.state.agent = agent

    yield

    logger.info("Closing application")


def init_app() -> FastAPI:
    from src.entrypoints.http import register_routes

    # Initialize FastAPI app
    app = FastAPI(
        title="Research Assistant Agent",
        description="A mini Research Assistant agent that answers natural-language questions about local documents",
        version="1.0.0",
        lifespan=_lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # register routes
    register_routes(app)
    return app


app = init_app()
