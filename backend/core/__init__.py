"""
HexLegIA Core Module
====================

Ce module contient la configuration centrale, les utilitaires et les dépendances
partagées entre les différents composants du backend.
"""

from .config import settings
from .logging import setup_logging
from .exceptions import (
    HexLegIAException,
    ConfigurationError,
    DatabaseError,
    SecurityError,
    EngineError,
    NotImplementedError,
)

__all__ = [
    "settings",
    "setup_logging",
    "HexLegIAException",
    "ConfigurationError",
    "DatabaseError",
    "SecurityError",
    "EngineError",
    "NotImplementedError",
]

# État du module
MODULE_STATUS = "IMPLEMENTED"
