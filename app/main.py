# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.core.database import engine, Base
import app.models  # Register models
from app.core.scheduler import scheduler, run_scheduled_store_inspections
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Start APScheduler cron job
    scheduler.add_job(
        run_scheduled_store_inspections, 
        "interval", 
        minutes=settings.CRAWL_INTERVAL_MINUTES
    )
    scheduler.start()
    
    yield
    
    scheduler.shutdown()
    await engine.dispose()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}
