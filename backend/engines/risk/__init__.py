"""
Risk Engine
==========

Moteur d'évaluation des risques.

Rôle :
- Évaluer les risques
- Analyser les vulnérabilités
- Calculer les scores de risque
- Générer des alertes

État : SCAFFOLD
"""

from .engine import RiskEngine
from .models import (
    RiskAssessmentRequest,
    RiskAssessmentResult,
    RiskLevel,
    RiskCategory,
)
from .exceptions import RiskAssessmentError

__all__ = [
    "RiskEngine",
    "RiskAssessmentRequest",
    "RiskAssessmentResult",
    "RiskLevel",
    "RiskCategory",
    "RiskAssessmentError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
