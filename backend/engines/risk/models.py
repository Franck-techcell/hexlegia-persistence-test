"""
Risk Engine Models
==================

Modèles pour le moteur de risque.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Niveau de risque."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """Catégorie de risque."""
    SECURITY = "security"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    REPUTATIONAL = "reputational"
    LEGAL = "legal"


class RiskAssessmentRequest(BaseModel):
    """Requête d'évaluation de risque."""
    name: str = Field(..., description="Nom de l'évaluation")
    description: Optional[str] = Field(default=None, description="Description de l'évaluation")
    target: str = Field(..., description="Cible de l'évaluation (ressource, action, etc.)")
    risk_categories: List[RiskCategory] = Field(default_factory=list, description="Catégories de risque à évaluer")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de l'évaluation")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte de l'évaluation")
    requester: Optional[str] = Field(default=None, description="Demandeur de l'évaluation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RiskAssessmentResult(BaseModel):
    """Résultat de l'évaluation de risque."""
    request: RiskAssessmentRequest
    overall_risk_level: RiskLevel
    category_risk_levels: Dict[RiskCategory, RiskLevel] = Field(default_factory=dict)
    risk_scores: Dict[str, float] = Field(default_factory=dict, description="Scores de risque (0-1)")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="Découvertes de l'évaluation")
    recommendations: List[str] = Field(default_factory=list, description="Recommandations")
    alerts: List[Dict[str, Any]] = Field(default_factory=list, description="Alertes générées")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: float = Field(default=0.0, description="Durée de l'évaluation en ms")


# État du module
MODULE_STATUS = "SCAFFOLD"
