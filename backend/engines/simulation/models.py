"""
Simulation Engine Models
=======================

Modèles pour le moteur de simulation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class SimulationType(str, Enum):
    """Type de simulation."""
    SCENARIO = "scenario"
    MONTE_CARLO = "monte_carlo"
    TIME_SERIES = "time_series"
    AGENT_BASED = "agent_based"
    SYSTEM_DYNAMICS = "system_dynamics"


class SimulationStatus(str, Enum):
    """Statut de la simulation."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SimulationRequest(BaseModel):
    """Requête de simulation."""
    simulation_type: SimulationType
    name: str = Field(..., description="Nom de la simulation")
    description: Optional[str] = Field(default=None, description="Description de la simulation")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de la simulation")
    initial_conditions: Dict[str, Any] = Field(default_factory=dict, description="Conditions initiales")
    constraints: List[Dict[str, Any]] = Field(default_factory=list, description="Contraintes de la simulation")
    requester: Optional[str] = Field(default=None, description="Demandeur de la simulation")
    priority: int = Field(default=0, description="Priorité de la simulation")
    timeout_seconds: float = Field(default=60.0, description="Timeout en secondes")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SimulationResult(BaseModel):
    """Résultat de la simulation."""
    request: SimulationRequest
    status: SimulationStatus
    results: Dict[str, Any] = Field(default_factory=dict, description="Résultats de la simulation")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Métriques calculées")
    visualizations: List[Dict[str, Any]] = Field(default_factory=list, description="Visualisations générées")
    warnings: List[str] = Field(default_factory=list, description="Avertissements")
    errors: List[str] = Field(default_factory=list, description="Erreurs rencontrées")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_seconds: float = Field(default=0.0, description="Durée de la simulation en secondes")


# État du module
MODULE_STATUS = "SCAFFOLD"
