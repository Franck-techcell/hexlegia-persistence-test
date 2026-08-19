"""
HexLegIA API Module
===================

Module contenant les routes, contrôleurs et middleware de l'API FastAPI.
"""

from .main import app
from .routes import health
from .middleware import (
    error_handler,
    request_id_middleware,
    audit_middleware,
    security_middleware,
)

__all__ = [
    "app",
    "health",
    "error_handler",
    "request_id_middleware",
    "audit_middleware",
    "security_middleware",
]

# État du module
MODULE_STATUS = "IMPLEMENTED"
