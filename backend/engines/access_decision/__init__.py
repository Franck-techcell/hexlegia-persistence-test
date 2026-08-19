"""
Access Decision Engine
=====================

Moteur de décision d'accès (version moteur).

Ce moteur est une version moteur du AccessDecisionEngine de la couche sécurité.
Il est conçu pour être intégré avec les autres moteurs et fournir des décisions
d'accès basées sur le contexte complet.

État : SCAFFOLD
"""

from .engine import AccessDecisionEngine
from .models import (
    AccessDecisionRequest,
    AccessDecisionResponse,
    DecisionType,
    SensitivityLevel,
)
from .exceptions import AccessDecisionError

__all__ = [
    "AccessDecisionEngine",
    "AccessDecisionRequest",
    "AccessDecisionResponse",
    "DecisionType",
    "SensitivityLevel",
    "AccessDecisionError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
