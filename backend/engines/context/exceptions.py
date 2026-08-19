"""
Context Engine Exceptions
=========================

Exceptions spécifiques au moteur de contexte.
"""

from backend.core.exceptions import EngineError


class ContextError(EngineError):
    """Exception de base pour le moteur de contexte."""
    
    def __init__(
        self,
        message: str,
        context_type: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"Context error ({context_type}): {message}",
            engine_name="ContextEngine",
            details={
                "context_type": context_type,
                **(details or {}),
            },
        )
        self.context_type = context_type


class ContextNotFoundError(ContextError):
    """Exception pour les contextes non trouvés."""
    
    def __init__(
        self,
        context_type: str,
        context_id: str,
    ):
        super().__init__(
            message=f"Context not found: {context_id}",
            context_type=context_type,
            details={"context_id": context_id},
        )
        self.context_id = context_id


class ContextValidationError(ContextError):
    """Exception pour les erreurs de validation de contexte."""
    
    def __init__(
        self,
        message: str,
        context_type: str = "unknown",
        validation_errors: list = None,
    ):
        super().__init__(
            message=message,
            context_type=context_type,
            details={"validation_errors": validation_errors},
        )
        self.validation_errors = validation_errors or []


class ContextConflictError(ContextError):
    """Exception pour les conflits de contexte."""
    
    def __init__(
        self,
        message: str,
        context_type: str = "unknown",
        conflicting_contexts: list = None,
    ):
        super().__init__(
            message=message,
            context_type=context_type,
            details={"conflicting_contexts": conflicting_contexts},
        )
        self.conflicting_contexts = conflicting_contexts or []


# État du module
MODULE_STATUS = "SCAFFOLD"
