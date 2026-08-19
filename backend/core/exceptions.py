"""
HexLegIA Custom Exceptions
==========================

Hiérarchie d'exceptions personnalisées pour l'application HexLegIA.
"""

from typing import Optional, Dict, Any
import traceback


class HexLegIAException(Exception):
    """Exception de base pour toutes les exceptions HexLegIA."""
    
    def __init__(
        self,
        message: str,
        code: str = "HEXLEGIA_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        self.trace_id = trace_id or self._generate_trace_id()
        self.stack_trace = traceback.format_stack()
    
    @staticmethod
    def _generate_trace_id() -> str:
        """Générer un ID de traçage unique."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir l'exception en dictionnaire pour la sérialisation."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "status_code": self.status_code,
                "trace_id": self.trace_id,
                "details": self.details,
            }
        }
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message} (trace: {self.trace_id})"


class ConfigurationError(HexLegIAException):
    """Exception pour les erreurs de configuration."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="CONFIGURATION_ERROR",
            status_code=500,
            details=details,
            trace_id=trace_id,
        )


class DatabaseError(HexLegIAException):
    """Exception pour les erreurs de base de données."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=503,
            details=details,
            trace_id=trace_id,
        )


class SecurityError(HexLegIAException):
    """Exception pour les erreurs de sécurité."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="SECURITY_ERROR",
            status_code=403,
            details=details,
            trace_id=trace_id,
        )


class AuthenticationError(SecurityError):
    """Exception pour les erreurs d'authentification."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            details=details,
            trace_id=trace_id,
        )
        self.code = "AUTHENTICATION_ERROR"
        self.status_code = 401


class AuthorizationError(SecurityError):
    """Exception pour les erreurs d'autorisation."""
    
    def __init__(
        self,
        message: str = "Authorization denied",
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            details=details,
            trace_id=trace_id,
        )
        self.code = "AUTHORIZATION_ERROR"
        self.status_code = 403


class EngineError(HexLegIAException):
    """Exception pour les erreurs des moteurs."""
    
    def __init__(
        self,
        message: str,
        engine_name: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=f"[{engine_name}] {message}",
            code="ENGINE_ERROR",
            status_code=500,
            details=details,
            trace_id=trace_id,
        )
        self.engine_name = engine_name


class NotImplementedError(HexLegIAException):
    """Exception pour les fonctionnalités non implémentées."""
    
    def __init__(
        self,
        message: str = "Feature not implemented",
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="NOT_IMPLEMENTED",
            status_code=501,
            details=details,
            trace_id=trace_id,
        )


class ValidationError(HexLegIAException):
    """Exception pour les erreurs de validation."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
            trace_id=trace_id,
        )


class AIProviderError(HexLegIAException):
    """Exception pour les erreurs des fournisseurs IA."""
    
    def __init__(
        self,
        message: str,
        provider_name: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=f"[{provider_name}] {message}",
            code="AI_PROVIDER_ERROR",
            status_code=502,
            details=details,
            trace_id=trace_id,
        )
        self.provider_name = provider_name


class AuditError(HexLegIAException):
    """Exception pour les erreurs d'audit."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        super().__init__(
            message=message,
            code="AUDIT_ERROR",
            status_code=500,
            details=details,
            trace_id=trace_id,
        )
