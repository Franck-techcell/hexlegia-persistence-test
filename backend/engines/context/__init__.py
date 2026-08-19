"""
Context Engine
=============

Moteur de gestion du contexte centralisé.

Rôle :
- Centraliser le contexte utilisateur
- Gérer le contexte organisationnel
- Maintenir le contexte temporel et réglementaire
- Fournir le contexte nécessaire aux décisions

État : SCAFFOLD
"""

from .engine import ContextEngine
from .models import (
    Context,
    UserContext,
    OrganizationContext,
    RequestContext,
    TemporalContext,
    RegulatoryContext,
    ContextType,
)
from .exceptions import ContextError

__all__ = [
    "ContextEngine",
    "Context",
    "UserContext",
    "OrganizationContext",
    "RequestContext",
    "TemporalContext",
    "RegulatoryContext",
    "ContextType",
    "ContextError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
