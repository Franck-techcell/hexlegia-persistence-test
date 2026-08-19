"""
Request ID Middleware
=====================

Middleware pour ajouter un identifiant unique à chaque requête.
"""

from fastapi import Request
from typing import Callable, Awaitable
from uuid import uuid4

from backend.core.logging import logger


async def request_id_middleware(
    request: Request, 
    call_next: Callable[[Request], Awaitable]
) -> Awaitable:
    """
    Ajouter un identifiant unique à chaque requête.
    
    Args:
        request: La requête HTTP.
        call_next: Fonction pour passer au middleware suivant.
    
    Returns:
        La réponse HTTP.
    """
    # Générer un identifiant de requête unique
    request_id = str(uuid4())[:8]
    
    # Ajouter à l'état de la requête
    request.state.request_id = request_id
    
    # Ajouter au contexte de logging
    logger.bind(request_id=request_id)
    
    # Ajouter aux headers de la réponse
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response


# État du module
MODULE_STATUS = "IMPLEMENTED"
