"""
HexLegIA API Routes
===================

Module contenant toutes les routes de l'API.
"""

from .health import router as health_router

__all__ = ["health_router"]

# État du module
MODULE_STATUS = "IMPLEMENTED"
