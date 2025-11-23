"""
FastAPI Application Entry Point - Production Ready
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import os

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered restaurant chatbot API",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    settings.FRONTEND_URL,
]

if os.getenv("ALLOWED_ORIGINS"):
    extra_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    allowed_origins.extend(extra_origins)

allowed_origins = list(set(filter(None, allowed_origins)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "status": "online",
        "version": settings.API_VERSION,
        "restaurant": settings.RESTAURANT_NAME,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


from app.routers import menu, chat, order, reservation

app.include_router(menu.router, prefix=f"/api/{settings.API_VERSION}", tags=["Menu"])
app.include_router(chat.router, prefix=f"/api/{settings.API_VERSION}", tags=["Chat"])
app.include_router(order.router, prefix=f"/api/{settings.API_VERSION}", tags=["Orders"])
app.include_router(reservation.router, prefix=f"/api/{settings.API_VERSION}", tags=["Reservations"])


@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.APP_NAME}...")
    print(f"Environment: {settings.ENVIRONMENT}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
