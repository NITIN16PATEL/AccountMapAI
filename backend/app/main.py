from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import auth, chatbot, dashboard, discovery, health, imports, inventory, privacy, providers
from app.core.config import settings
from app.db.session import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AccountMap AI API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


@app.get("/health")
@limiter.limit("60/minute")
def health_check(request: Request):
    return {"status": "ok", "app": settings.app_name}


@app.get("/")
def root():
    return {"message": "AccountMap AI API is running."}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(discovery.router, prefix="/api/discovery", tags=["discovery"])
app.include_router(imports.router, prefix="/api/imports", tags=["imports"])
app.include_router(privacy.router, prefix="/api/privacy", tags=["privacy"])
app.include_router(providers.router, prefix="/api/providers", tags=["providers"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(health.router, prefix="/api", tags=["health"])
