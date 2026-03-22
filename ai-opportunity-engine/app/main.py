from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.tasks.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    try:
        yield
    finally:
        stop_scheduler()


app = FastAPI(title="AI Opportunity Engine", lifespan=lifespan)
app.include_router(router)
