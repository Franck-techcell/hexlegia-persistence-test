"""
Access Decision Engine Models
=============================

Modèles pour le moteur de décision d'accès.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class DecisionType(str, Enum):
    """Type de décision."""
    ALLOWED = "allowed"
    DENIED = "denied"
    PENDING = "pending"
    CONDITIONAL = "conditional"


class SensitivityLevel(str, Enum):
    """Niveau de sensibilité."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class RequesterType(str, Enum):
    """Type de demandeur."""
    HUMAN = "human"
    AI = "ai"
    SERVICE = "service"
    SYSTEM = "system"


class AccessDecisionRequest(BaseModel):
    """Requête de décision d'accès."""
    requester: str = Field(..., description="Identité du demandeur")
    requester_type: RequesterType = Field(default=RequesterType.HUMAN, description="Type du demandeur")
    resource: str = Field(..., description="Ressource demandée")
    action: str = Field(..., description="Action demandée")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte de la requête")
    justification: Optional[str] = Field(default=None, description="Justification de la requête")
    sensitivity_level: SensitivityLevel = Field(default=SensitivityLevel.INTERNAL, description="Niveau de sensibilité")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(default=None, description="ID de la requête")


class AccessDecisionResponse(BaseModel):
    """Réponse de décision d'accès."""
    request: AccessDecisionRequest
    decision: DecisionType
    allowed: bool
    reason: Optional[str] = Field(default=None, description="Raison de la décision")
    justification: Optional[str] = Field(default=None, description="Justification de la décision")
    conditions: List[str] = Field(default_factory=list, description="Conditions pour l'accès")
    policies_applied: List[str] = Field(default_factory=list, description="Politiques appliquées")
    audit_trace: Dict[str, Any] = Field(default_factory=dict, description="Trace d'audit")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence_score: float = Field(default=0.0, description="Score de confiance (0-1)")


class AccessDecisionAudit(BaseModel):
    """Audit de décision d'accès."""
    request_id: str
    requester: str
    requester_type: RequesterType
    resource: str
    action: str
    decision: DecisionType
    allowed: bool
    reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# État du module
MODULE_STATUS = "SCAFFOLD"
