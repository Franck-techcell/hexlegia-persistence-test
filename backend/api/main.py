"""
HexLegIA FastAPI Application
=============================

Point d'entrée principal de l'application FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import logging

from backend.core.config import settings
from backend.core.logging import setup_logging, logger
from backend.core.exceptions import HexLegIAException

from .routes import health
from .middleware import (
    request_id_middleware,
    audit_middleware,
    security_middleware,
    error_handler,
)

# Initialiser le logging
setup_logging()

# Créer l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter les middlewares
app.middleware("http")(request_id_middleware)
app.middleware("http")(audit_middleware)
app.middleware("http")(security_middleware)

# Gestionnaire d'erreurs global
@app.exception_handler(HexLegIAException)
async def hexlegia_exception_handler(request: Request, exc: HexLegIAException):
    """Gestionnaire d'erreurs pour les exceptions HexLegIA."""
    logger.error(
        "HexLegIA Exception",
        error_code=exc.code,
        message=exc.message,
        status_code=exc.status_code,
        trace_id=exc.trace_id,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'erreurs générique."""
    logger.error(
        "Unexpected Exception",
        error=str(exc),
        type=type(exc).__name__,
        extra={"request": str(request)},
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "status_code": 500,
            }
        },
    )


# Inclure les routes
app.include_router(health.router, prefix="/health", tags=["health"])

# Hook de démarrage
@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'application."""
    logger.info(
        "Application startup",
        app_name=settings.app_name,
        app_version=settings.app_version,
        debug=settings.debug,
        host=settings.host,
        port=settings.port,
    )
    
    # Initialisation des moteurs (à implémenter)
    from backend.engines import init_engines
    await init_engines()
    
    logger.info("All engines initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Actions à effectuer à l'arrêt de l'application."""
    logger.info("Application shutdown")
    
    # Nettoyage des moteurs (à implémenter)
    from backend.engines import cleanup_engines
    await cleanup_engines()


# État du module
MODULE_STATUS = "IMPLEMENTED"
