"""
HexLegIA Logging Configuration
==============================

Configuration centralisée du logging pour l'application HexLegIA.
"""

import logging
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime
import structlog
from .config import settings


def setup_logging() -> None:
    """Configurer le système de logging pour l'application."""
    
    # Niveau de log global
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    
    # Désactiver les logs des bibliothèques tierces (trop verbeuses)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    # Configuration de structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _add_trace_id,
            _add_timestamp,
            _format_log,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Remplacer le logger standard par structlog
    structlog.stdlib.install_logger_factory()


def _add_trace_id(logger: structlog.BoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Ajouter un trace_id unique à chaque log."""
    import uuid
    if "trace_id" not in event_dict:
        event_dict["trace_id"] = str(uuid.uuid4())[:8]
    return event_dict


def _add_timestamp(logger: structlog.BoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Ajouter un timestamp ISO à chaque log."""
    event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return event_dict


def _format_log(logger: structlog.BoundLogger, method_name: str, event_dict: Dict[str, Any]) -> str:
    """Formater le log selon le format configuré."""
    if settings.log_format == "json":
        # Supprimer les champs qui ne sont pas sérialisables
        clean_dict = {k: v for k, v in event_dict.items() if _is_serializable(v)}
        return json.dumps(clean_dict, default=str)
    else:
        # Format texte
        level = event_dict.get("level", "INFO").upper()
        timestamp = event_dict.get("timestamp", "")
        trace_id = event_dict.get("trace_id", "")
        message = event_dict.get("event", "")
        logger_name = event_dict.get("logger", "")
        
        # Extraire les champs supplémentaires
        extra_fields = {k: v for k, v in event_dict.items() 
                       if k not in ["level", "timestamp", "trace_id", "event", "logger"]}
        
        if extra_fields:
            extra_str = " | ".join(f"{k}={v}" for k, v in extra_fields.items())
            return f"[{timestamp}] [{level}] [{trace_id}] [{logger_name}] {message} | {extra_str}"
        else:
            return f"[{timestamp}] [{level}] [{trace_id}] [{logger_name}] {message}"


def _is_serializable(value: Any) -> bool:
    """Vérifier si une valeur est sérialisable en JSON."""
    try:
        json.dumps(value, default=str)
        return True
    except (TypeError, ValueError):
        return False


# Logger global pour l'application
logger = structlog.get_logger("hexlegia")


def get_logger(name: str) -> structlog.BoundLogger:
    """Obtenir un logger avec un nom spécifique."""
    return structlog.get_logger(name)


# État du module
MODULE_STATUS = "IMPLEMENTED"
