from contextlib import asynccontextmanager
from src.core.settings import settings
from fastapi import FastAPI
from src.core.logging import logger
from sqlmodel import SQLModel
from src.core.database import engine
from src.routes.address import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized.")
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(router, prefix="/api", tags=["Addresses"])


# @app.on_event("startup")
# def on_startup():
#     logger.info("Initializing database...")
#     SQLModel.metadata.create_all(engine)
#     logger.info("Database initialized.")
