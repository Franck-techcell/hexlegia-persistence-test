"""
HexLegIA Security Module
========================

Module dédié à la sécurité : authentification, autorisation, audit.
"""

from .access_control import AccessDecisionEngine, AccessDecision
from .authentication import AuthenticationService
from .authorization import AuthorizationService
from .audit import AuditService
from .models import (
    User,
    Role,
    Permission,
    AccessRequest,
    AccessDecision as AccessDecisionModel,
)
from .policies import BasePolicy, RBACPolicy, ABACPolicy

__all__ = [
    "AccessDecisionEngine",
    "AccessDecision",
    "AuthenticationService",
    "AuthorizationService",
    "AuditService",
    "User",
    "Role",
    "Permission",
    "AccessRequest",
    "AccessDecisionModel",
    "BasePolicy",
    "RBACPolicy",
    "ABACPolicy",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
