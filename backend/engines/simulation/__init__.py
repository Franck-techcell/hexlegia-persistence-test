"""
Simulation Engine
================

Moteur de simulation de scénarios.

Rôle :
- Simuler des scénarios complexes
- Tester des hypothèses
- Évaluer des impacts
- Générer des prédictions

État : SCAFFOLD
"""

from .engine import SimulationEngine
from .models import (
    SimulationRequest,
    SimulationResult,
    SimulationType,
    SimulationStatus,
)
from .exceptions import SimulationError

__all__ = [
    "SimulationEngine",
    "SimulationRequest",
    "SimulationResult",
    "SimulationType",
    "SimulationStatus",
    "SimulationError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
