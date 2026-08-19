"""
Risk Engine Exceptions
======================

Exceptions spécifiques au moteur de risque.
"""

from backend.core.exceptions import EngineError


class RiskAssessmentError(EngineError):
    """Exception de base pour le moteur de risque."""
    
    def __init__(
        self,
        message: str,
        assessment_name: str = "unknown",
        target: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"Risk assessment error ({assessment_name}, {target}): {message}",
            engine_name="RiskEngine",
            details={
                "assessment_name": assessment_name,
                "target": target,
                **(details or {}),
            },
        )
        self.assessment_name = assessment_name
        self.target = target


# État du module
MODULE_STATUS = "SCAFFOLD"
