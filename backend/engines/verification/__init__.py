"""
Verification Engine
===================

Moteur de vérification des données et identités.

Rôle :
- Vérifier l'intégrité des données
- Valider les identités
- Vérifier les signatures et certificats
- Détecter les anomalies

État : SCAFFOLD
"""

from .engine import VerificationEngine
from .models import (
    VerificationRequest,
    VerificationResult,
    VerificationType,
    VerificationStatus,
)
from .exceptions import VerificationError

__all__ = [
    "VerificationEngine",
    "VerificationRequest",
    "VerificationResult",
    "VerificationType",
    "VerificationStatus",
    "VerificationError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
