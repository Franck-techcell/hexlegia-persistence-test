"""
Audit Middleware
===============

Middleware pour le traçage des opérations importantes.
"""

from fastapi import Request
from typing import Callable, Awaitable, Dict, Any
from datetime import datetime
import json

from backend.core.config import settings
from backend.core.logging import logger
from backend.core.exceptions import AuditError


async def audit_middleware(
    request: Request, 
    call_next: Callable[[Request], Awaitable]
) -> Awaitable:
    """
    Traçage des opérations pour l'audit.
    
    Args:
        request: La requête HTTP.
        call_next: Fonction pour passer au middleware suivant.
    
    Returns:
        La réponse HTTP.
    """
    if not settings.audit_enabled:
        return await call_next(request)
    
    # Ignorer les requêtes de santé
    if request.url.path == "/health" or request.url.path == "/health/":
        return await call_next(request)
    
    # Capturer les informations de la requête
    audit_data: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": getattr(request.state, "request_id", "unknown"),
        "method": request.method,
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "client": {
            "host": request.client.host if request.client else None,
            "port": request.client.port if request.client else None,
        },
        "headers": _sanitize_headers(dict(request.headers)),
    }
    
    # Essayer de capturer le corps de la requête (si JSON)
    try:
        if request.headers.get("content-type") == "application/json":
            body = await request.json()
            audit_data["request_body"] = body
    except Exception:
        pass
    
    # Ajouter l'utilisateur si authentifié
    user_info = _get_user_info(request)
    if user_info:
        audit_data["user"] = user_info
    
    # Exécuter la requête
    response = await call_next(request)
    
    # Capturer les informations de la réponse
    audit_data["response"] = {
        "status_code": response.status_code,
        "headers": _sanitize_headers(dict(response.headers)),
    }
    
    # Essayer de capturer le corps de la réponse (si JSON)
    try:
        if response.headers.get("content-type") == "application/json":
            response_body = json.loads(response.body)
            audit_data["response"]["body"] = response_body
    except Exception:
        pass
    
    # Écrire dans le log d'audit
    try:
        _write_audit_log(audit_data)
    except AuditError as e:
        logger.error("Failed to write audit log", error=str(e), audit_data=audit_data)
    
    return response


def _sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """Nettoyer les headers pour supprimer les informations sensibles."""
    sensitive_keys = ["authorization", "cookie", "set-cookie", "x-api-key", "x-secret"]
    sanitized = {}
    
    for key, value in headers.items():
        lower_key = key.lower()
        if any(sensitive in lower_key for sensitive in sensitive_keys):
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    
    return sanitized


def _get_user_info(request: Request) -> Dict[str, Any]:
    """Extraire les informations utilisateur de la requête."""
    # À implémenter avec l'authentification
    # Pour l'instant, retourner None
    return None


def _write_audit_log(audit_data: Dict[str, Any]) -> None:
    """Écrire les données d'audit dans le fichier de log."""
    if not settings.audit_enabled:
        return
    
    try:
        # Formater les données
        log_entry = {
            "audit": audit_data,
            "severity": "INFO",
        }
        
        # Écrire dans le fichier
        with open(settings.audit_log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Also log to stdout
        logger.info("Audit log", **audit_data)
        
    except Exception as e:
        raise AuditError(
            message=f"Failed to write audit log: {str(e)}",
            details={"audit_data": audit_data},
        )


# État du module
MODULE_STATUS = "IMPLEMENTED"
