"""
Verification Engine Exceptions
==============================

Exceptions spécifiques au moteur de vérification.
"""

from backend.core.exceptions import EngineError


class VerificationError(EngineError):
    """Exception de base pour le moteur de vérification."""
    
    def __init__(
        self,
        message: str,
        verification_type: str = "unknown",
        target: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"Verification error ({verification_type}): {message}",
            engine_name="VerificationEngine",
            details={
                "verification_type": verification_type,
                "target": target,
                **(details or {}),
            },
        )
        self.verification_type = verification_type
        self.target = target


class VerificationTimeoutError(VerificationError):
    """Exception pour les timeouts de vérification."""
    
    def __init__(
        self,
        message: str = "Verification timed out",
        verification_type: str = "unknown",
        target: str = "unknown",
        timeout_seconds: float = 0,
    ):
        super().__init__(
            message=message,
            verification_type=verification_type,
            target=target,
            details={"timeout_seconds": timeout_seconds},
        )
        self.timeout_seconds = timeout_seconds


class VerificationValidationError(VerificationError):
    """Exception pour les erreurs de validation."""
    
    def __init__(
        self,
        message: str,
        verification_type: str = "unknown",
        target: str = "unknown",
        validation_errors: list = None,
    ):
        super().__init__(
            message=message,
            verification_type=verification_type,
            target=target,
            details={"validation_errors": validation_errors},
        )
        self.validation_errors = validation_errors or []


class VerificationNotSupportedError(VerificationError):
    """Exception pour les types de vérification non supportés."""
    
    def __init__(
        self,
        verification_type: str,
        target: str = "unknown",
    ):
        super().__init__(
            message=f"Verification type not supported: {verification_type}",
            verification_type=verification_type,
            target=target,
        )


# État du module
MODULE_STATUS = "SCAFFOLD"
