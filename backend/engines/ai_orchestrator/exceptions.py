"""
AI Orchestrator Exceptions
==========================

Exceptions spécifiques à l'orchestrateur IA.
"""

from backend.core.exceptions import EngineError, AIProviderError


class AIOrchestratorError(EngineError):
    """Exception de base pour l'orchestrateur IA."""
    
    def __init__(
        self,
        message: str,
        provider_type: str = "unknown",
        model: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"AI Orchestrator error ({provider_type}, {model}): {message}",
            engine_name="AIOrchestrator",
            details={
                "provider_type": provider_type,
                "model": model,
                **(details or {}),
            },
        )
        self.provider_type = provider_type
        self.model = model


class NoProviderAvailableError(AIOrchestratorError):
    """Exception pour aucun fournisseur disponible."""
    
    def __init__(
        self,
        message: str = "No AI provider available",
        requested_provider: str = None,
        available_providers: list = None,
    ):
        super().__init__(
            message=message,
            provider_type="none",
            model="none",
            details={
                "requested_provider": requested_provider,
                "available_providers": available_providers,
            },
        )
        self.requested_provider = requested_provider
        self.available_providers = available_providers or []


class ProviderNotConfiguredError(AIOrchestratorError):
    """Exception pour un fournisseur non configuré."""
    
    def __init__(
        self,
        provider_type: str,
        message: str = "Provider not configured",
    ):
        super().__init__(
            message=message,
            provider_type=provider_type,
            model="unknown",
        )


class ModelNotAvailableError(AIOrchestratorError):
    """Exception pour un modèle non disponible."""
    
    def __init__(
        self,
        provider_type: str,
        model: str,
        available_models: list = None,
    ):
        super().__init__(
            message=f"Model not available: {model}",
            provider_type=provider_type,
            model=model,
            details={"available_models": available_models},
        )
        self.available_models = available_models or []


class AIRequestTimeoutError(AIOrchestratorError):
    """Exception pour un timeout de requête IA."""
    
    def __init__(
        self,
        provider_type: str,
        model: str,
        timeout_seconds: float,
    ):
        super().__init__(
            message=f"AI request timed out after {timeout_seconds}s",
            provider_type=provider_type,
            model=model,
            details={"timeout_seconds": timeout_seconds},
        )
        self.timeout_seconds = timeout_seconds


class AIRequestError(AIOrchestratorError):
    """Exception pour une erreur de requête IA."""
    
    def __init__(
        self,
        provider_type: str,
        model: str,
        error_message: str,
        error_code: str = None,
    ):
        super().__init__(
            message=f"AI request failed: {error_message}",
            provider_type=provider_type,
            model=model,
            details={
                "error_message": error_message,
                "error_code": error_code,
            },
        )
        self.error_message = error_message
        self.error_code = error_code


# État du module
MODULE_STATUS = "SCAFFOLD"
