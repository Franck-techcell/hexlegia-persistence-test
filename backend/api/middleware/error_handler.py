"""
Error Handler Middleware
=======================

Middleware pour la gestion centralisée des erreurs.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import logging

from backend.core.exceptions import HexLegIAException
from backend.core.logging import logger


async def error_handler(
    request: Request, 
    call_next: Callable[[Request], Awaitable]
) -> Awaitable:
    """
    Gestion centralisée des erreurs.
    
    Args:
        request: La requête HTTP.
        call_next: Fonction pour passer au middleware suivant.
    
    Returns:
        La réponse HTTP.
    """
    try:
        return await call_next(request)
    except HexLegIAException as e:
        logger.error(
            "HexLegIA Exception caught",
            error_code=e.code,
            message=e.message,
            status_code=e.status_code,
            trace_id=e.trace_id,
            details=e.details,
        )
        return JSONResponse(
            status_code=e.status_code,
            content=e.to_dict(),
        )
    except Exception as e:
        logger.error(
            "Unexpected exception",
            error=str(e),
            type=type(e).__name__,
            request_path=str(request.url),
            request_method=request.method,
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


# État du module
MODULE_STATUS = "IMPLEMENTED"
