"""
FastAPI Application Entry Point
This is the main file that runs the entire API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import menu, chat

# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered restaurant chatbot API for menu queries, orders, and reservations",
    version=settings.API_VERSION,
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# CORS middleware - allows frontend to call API
# In production, replace "*" with your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint - health check
@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint - verify API is running
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "status": "online",
        "version": settings.API_VERSION,
        "restaurant": settings.RESTAURANT_NAME,
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "debug_mode": settings.DEBUG
    }


# Include routers (we'll add more in next phases)
app.include_router(
    menu.router,
    prefix=f"/api/{settings.API_VERSION}",
    tags=["Menu"]
)

app.include_router(
    chat.router,
    prefix=f"/api/{settings.API_VERSION}",
    tags=["Chat"]
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Runs when application starts
    """
    print(f"\n{'='*50}")
    print(f"🚀 {settings.APP_NAME} Starting...")
    print(f"{'='*50}")
    print(f"📍 Restaurant: {settings.RESTAURANT_NAME}")
    print(f"🕐 Hours: {settings.RESTAURANT_HOURS}")
    print(f"🚚 Delivery: {'Available' if settings.DELIVERY_AVAILABLE else 'Not Available'}")
    print(f"📚 Docs: http://localhost:8000/docs")
    print(f"{'='*50}\n")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when application shuts down
    """
    print(f"\n{'='*50}")
    print(f"👋 {settings.APP_NAME} Shutting Down...")
    print(f"{'='*50}\n")


# For running directly: python app/main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
