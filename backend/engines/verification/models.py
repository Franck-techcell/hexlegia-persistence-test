"""
Verification Engine Models
==========================

Modèles pour le moteur de vérification.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class VerificationType(str, Enum):
    """Type de vérification."""
    IDENTITY = "identity"
    DATA = "data"
    SIGNATURE = "signature"
    CERTIFICATE = "certificate"
    INTEGRITY = "integrity"
    AUTHENTICITY = "authenticity"


class VerificationStatus(str, Enum):
    """Statut de la vérification."""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    ERROR = "error"


class VerificationRequest(BaseModel):
    """Requête de vérification."""
    verification_type: VerificationType
    target: str = Field(..., description="Cible de la vérification (ID, donnée, certificat, etc.)")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Données à vérifier")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte de la vérification")
    requester: Optional[str] = Field(default=None, description="Demandeur de la vérification")
    priority: int = Field(default=0, description="Priorité de la vérification")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class VerificationResult(BaseModel):
    """Résultat de la vérification."""
    request: VerificationRequest
    status: VerificationStatus
    result: Optional[Dict[str, Any]] = Field(default=None, description="Résultat détaillé")
    score: Optional[float] = Field(default=None, description="Score de confiance (0-1)")
    issues: List[str] = Field(default_factory=list, description="Liste des problèmes détectés")
    warnings: List[str] = Field(default_factory=list, description="Liste des avertissements")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: float = Field(default=0.0, description="Durée de la vérification en ms")


class VerificationAudit(BaseModel):
    """Audit de la vérification."""
    request_id: str
    verification_type: VerificationType
    target: str
    status: VerificationStatus
    requester: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Dict[str, Any] = Field(default_factory=dict)


# État du module
MODULE_STATUS = "SCAFFOLD"
