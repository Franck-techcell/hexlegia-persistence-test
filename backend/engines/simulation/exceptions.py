"""
Simulation Engine Exceptions
============================

Exceptions spécifiques au moteur de simulation.
"""

from backend.core.exceptions import EngineError


class SimulationError(EngineError):
    """Exception de base pour le moteur de simulation."""
    
    def __init__(
        self,
        message: str,
        simulation_type: str = "unknown",
        simulation_name: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"Simulation error ({simulation_type}, {simulation_name}): {message}",
            engine_name="SimulationEngine",
            details={
                "simulation_type": simulation_type,
                "simulation_name": simulation_name,
                **(details or {}),
            },
        )
        self.simulation_type = simulation_type
        self.simulation_name = simulation_name


class SimulationTimeoutError(SimulationError):
    """Exception pour les timeouts de simulation."""
    
    def __init__(
        self,
        simulation_type: str,
        simulation_name: str,
        timeout_seconds: float,
    ):
        super().__init__(
            message=f"Simulation timed out after {timeout_seconds}s",
            simulation_type=simulation_type,
            simulation_name=simulation_name,
            details={"timeout_seconds": timeout_seconds},
        )
        self.timeout_seconds = timeout_seconds


class SimulationValidationError(SimulationError):
    """Exception pour les erreurs de validation de simulation."""
    
    def __init__(
        self,
        message: str,
        simulation_type: str = "unknown",
        simulation_name: str = "unknown",
        validation_errors: list = None,
    ):
        super().__init__(
            message=message,
            simulation_type=simulation_type,
            simulation_name=simulation_name,
            details={"validation_errors": validation_errors},
        )
        self.validation_errors = validation_errors or []


# État du module
MODULE_STATUS = "SCAFFOLD"
