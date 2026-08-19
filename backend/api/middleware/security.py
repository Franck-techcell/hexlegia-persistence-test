"""
Security Middleware
==================

Middleware pour la sécurité et le contrôle d'accès.
"""

from fastapi import Request, HTTPException, status
from typing import Callable, Awaitable
from functools import wraps

from backend.core.logging import logger
from backend.security.access_control import AccessDecisionEngine


async def security_middleware(
    request: Request, 
    call_next: Callable[[Request], Awaitable]
) -> Awaitable:
    """
    Middleware de sécurité pour le contrôle d'accès.
    
    Args:
        request: La requête HTTP.
        call_next: Fonction pour passer au middleware suivant.
    
    Returns:
        La réponse HTTP.
    """
    # Ignorer les requêtes de santé
    if request.url.path == "/health" or request.url.path == "/health/":
        return await call_next(request)
    
    # Vérifier l'accès via AccessDecisionEngine
    access_engine = AccessDecisionEngine()
    
    try:
        # Extraire les informations de la requête
        requester = _extract_requester(request)
        resource = request.url.path
        action = request.method
        context = {
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
        }
        
        # Vérifier l'accès
        decision = await access_engine.check_access(
            requester=requester,
            resource=resource,
            action=action,
            context=context,
        )
        
        if not decision.allowed:
            logger.warning(
                "Access denied",
                requester=str(requester),
                resource=resource,
                action=action,
                reason=decision.reason,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": {
                        "code": "ACCESS_DENIED",
                        "message": decision.reason or "Access denied",
                        "requester": str(requester),
                        "resource": resource,
                        "action": action,
                    }
                },
            )
        
        # Ajouter les informations de décision à la requête
        request.state.access_decision = decision
        
    except Exception as e:
        logger.error("Security middleware error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": "SECURITY_ERROR", "message": str(e)}},
        )
    
    return await call_next(request)


def _extract_requester(request: Request) -> str:
    """Extraire l'identité du demandeur de la requête."""
    # À implémenter avec l'authentification
    # Pour l'instant, retourner "anonymous"
    return "anonymous"


# Décorateur pour le contrôle d'accès manuel
def require_access(
    resource: str,
    action: str,
    requester_type: str = "user",
):
    """
    Décorateur pour vérifier l'accès à une ressource spécifique.
    
    Args:
        resource: La ressource à protéger.
        action: L'action à autoriser.
        requester_type: Le type de demandeur (user, ai, service).
    
    Returns:
        Fonction décorateur.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extraire la requête des arguments
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": {"code": "INVALID_REQUEST", "message": "Request object required"}},
                )
            
            # Vérifier l'accès
            access_engine = AccessDecisionEngine()
            requester = _extract_requester(request)
            
            decision = await access_engine.check_access(
                requester=requester,
                resource=resource,
                action=action,
                context={"requester_type": requester_type},
            )
            
            if not decision.allowed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": {
                            "code": "ACCESS_DENIED",
                            "message": decision.reason or "Access denied",
                        }
                    },
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# État du module
MODULE_STATUS = "IMPLEMENTED"
