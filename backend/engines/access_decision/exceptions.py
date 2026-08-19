"""
Access Decision Engine Exceptions
=================================

Exceptions spécifiques au moteur de décision d'accès.
"""

from backend.core.exceptions import EngineError


class AccessDecisionError(EngineError):
    """Exception de base pour le moteur de décision d'accès."""
    
    def __init__(
        self,
        message: str,
        requester: str = "unknown",
        resource: str = "unknown",
        action: str = "unknown",
        details: dict = None,
    ):
        super().__init__(
            message=f"Access decision error: {message}",
            engine_name="AccessDecisionEngine",
            details={
                "requester": requester,
                "resource": resource,
                "action": action,
                **(details or {}),
            },
        )
        self.requester = requester
        self.resource = resource
        self.action = action


class AccessDeniedError(AccessDecisionError):
    """Exception pour les accès refusés."""
    
    def __init__(
        self,
        requester: str,
        resource: str,
        action: str,
        reason: str = "Access denied",
    ):
        super().__init__(
            message=f"Access denied to {resource} for {action}",
            requester=requester,
            resource=resource,
            action=action,
            details={"reason": reason},
        )
        self.reason = reason


class PolicyEvaluationError(AccessDecisionError):
    """Exception pour les erreurs d'évaluation de politique."""
    
    def __init__(
        self,
        message: str,
        policy_name: str,
        requester: str = "unknown",
        resource: str = "unknown",
        action: str = "unknown",
    ):
        super().__init__(
            message=f"Policy evaluation error: {message}",
            requester=requester,
            resource=resource,
            action=action,
            details={"policy_name": policy_name},
        )
        self.policy_name = policy_name


class InsufficientContextError(AccessDecisionError):
    """Exception pour le contexte insuffisant."""
    
    def __init__(
        self,
        requester: str,
        resource: str,
        action: str,
        missing_context: List[str],
    ):
        super().__init__(
            message="Insufficient context for access decision",
            requester=requester,
            resource=resource,
            action=action,
            details={"missing_context": missing_context},
        )
        self.missing_context = missing_context


# État du module
MODULE_STATUS = "SCAFFOLD"
