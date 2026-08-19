"""
HexLegIA API Middleware
=======================

Module contenant tous les middlewares de l'API.
"""

from .request_id import request_id_middleware
from .audit import audit_middleware
from .security import security_middleware
from .error_handler import error_handler

__all__ = [
    "request_id_middleware",
    "audit_middleware",
    "security_middleware",
    "error_handler",
]

# État du module
MODULE_STATUS = "IMPLEMENTED"
