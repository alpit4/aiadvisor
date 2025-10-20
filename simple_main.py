"""
Simplified main script without LiveKit dependencies
"""
import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import init_db
from src.supervisor_ui_simple import create_supervisor_app
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    print("✅ Database initialized")
    yield
    print("Shutting down...")


def create_app():
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Frontdesk AI Supervisor",
        description="Human-in-the-loop AI system for customer service",
        lifespan=lifespan
    )
    
    # Include supervisor UI routes
    supervisor_app = create_supervisor_app()
    app.mount("/supervisor", supervisor_app)
    
    @app.get("/")
    async def root():
        return {
            "message": "Frontdesk AI Supervisor System",
            "status": "running",
            "supervisor_ui": "/supervisor",
            "note": "This is a simplified version without LiveKit integration"
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app


if __name__ == "__main__":
    # Start the web server
    app = create_app()
    
    print("Starting Frontdesk AI Supervisor System")
    print("=" * 50)
    print("Supervisor Dashboard: http://localhost:8000/supervisor")
    print("Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
