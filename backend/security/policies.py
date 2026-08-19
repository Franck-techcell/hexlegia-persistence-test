"""
Security Policies
================

Politiques d'accès pour le moteur de décision.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime

from backend.core.logging import logger
from .models import (
    AccessRequest,
    AccessDecision,
    DecisionType,
    UserType,
    SensitivityLevel,
)


class BasePolicy(ABC):
    """Classe de base pour les politiques d'accès."""
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        priority: int = 0,
        is_active: bool = True,
    ):
        """
        Initialiser la politique.
        
        Args:
            name: Nom de la politique.
            description: Description de la politique.
            priority: Priorité (plus élevé = évalué en premier).
            is_active: Si la politique est active.
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.is_active = is_active
        self.created_at = datetime.utcnow()
    
    @abstractmethod
    async def evaluate(self, request: AccessRequest) -> Optional[AccessDecision]:
        """
        Évaluer une requête d'accès.
        
        Args:
            request: La requête d'accès à évaluer.
        
        Returns:
            AccessDecision: La décision d'accès, ou None si la politique ne s'applique pas.
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, priority={self.priority}, active={self.is_active})"


class RBACPolicy(BasePolicy):
    """
    Politique basée sur les rôles (Role-Based Access Control).
    
    Cette politique vérifie si le demandeur a le rôle nécessaire pour accéder
    à la ressource avec l'action demandée.
    """
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        priority: int = 10,
        is_active: bool = True,
    ):
        super().__init__(name, description, priority, is_active)
        # Structure: {role_name: {resource: [actions]}}
        self.roles: Dict[str, Dict[str, List[str]]] = {}
        # Structure: {user_id: [role_names]}
        self.user_roles: Dict[str, List[str]] = {}
    
    async def evaluate(self, request: AccessRequest) -> Optional[AccessDecision]:
        """Évaluer la requête selon les rôles."""
        logger.debug(
            "RBACPolicy evaluating",
            policy=self.name,
            requester=request.requester,
            resource=request.resource,
            action=request.action,
        )
        
        # Obtenir les rôles de l'utilisateur
        user_roles = self.user_roles.get(request.requester, [])
        
        if not user_roles:
            logger.debug(
                "No roles found for user",
                user=request.requester,
            )
            return None
        
        # Vérifier chaque rôle
        for role_name in user_roles:
            role_permissions = self.roles.get(role_name, {})
            
            if role_name not in self.roles:
                continue
            
            # Vérifier si la ressource est dans les permissions du rôle
            if request.resource in role_permissions:
                allowed_actions = role_permissions[request.resource]
                
                if request.action in allowed_actions or "*" in allowed_actions:
                    logger.debug(
                        "Access GRANTED by RBAC",
                        user=request.requester,
                        role=role_name,
                        resource=request.resource,
                        action=request.action,
                    )
                    return AccessDecision(
                        request=request,
                        allowed=True,
                        decision=DecisionType.ALLOWED,
                        reason=f"Allowed by role {role_name}",
                        justification=request.justification,
                        policies_applied=[self.name],
                        audit_trace={
                            "policy": self.name,
                            "role": role_name,
                            "decision": "allowed",
                        },
                        timestamp=datetime.utcnow(),
                    )
        
        # Si aucun rôle n'autorise l'accès
        logger.debug(
            "Access DENIED by RBAC",
            user=request.requester,
            roles=user_roles,
            resource=request.resource,
            action=request.action,
        )
        
        return AccessDecision(
            request=request,
            allowed=False,
            decision=DecisionType.DENIED,
            reason=f"No role grants access to {request.resource} with {request.action}",
            justification=request.justification,
            policies_applied=[self.name],
            audit_trace={
                "policy": self.name,
                "roles": user_roles,
                "decision": "denied",
            },
            timestamp=datetime.utcnow(),
        )
    
    def add_role(self, role_name: str, description: Optional[str] = None) -> None:
        """Ajouter un rôle."""
        if role_name not in self.roles:
            self.roles[role_name] = {}
        logger.info(f"Role added: {role_name}")
    
    def add_permission(
        self,
        role_name: str,
        resource: str,
        actions: List[str],
    ) -> None:
        """Ajouter une permission à un rôle."""
        if role_name not in self.roles:
            self.add_role(role_name)
        
        if resource not in self.roles[role_name]:
            self.roles[role_name][resource] = []
        
        self.roles[role_name][resource].extend(actions)
        # Supprimer les doublons
        self.roles[role_name][resource] = list(set(self.roles[role_name][resource]))
        
        logger.info(f"Permission added: {role_name} -> {resource}:{actions}")
    
    def assign_role_to_user(self, user_id: str, role_name: str) -> None:
        """Assigner un rôle à un utilisateur."""
        if user_id not in self.user_roles:
            self.user_roles[user_id] = []
        
        if role_name not in self.user_roles[user_id]:
            self.user_roles[user_id].append(role_name)
        
        logger.info(f"Role assigned: {role_name} to {user_id}")


class ABACPolicy(BasePolicy):
    """
    Politique basée sur les attributs (Attribute-Based Access Control).
    
    Cette politique vérifie si le demandeur a les attributs nécessaires pour
    accéder à la ressource avec l'action demandée.
    """
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        priority: int = 20,
        is_active: bool = True,
    ):
        super().__init__(name, description, priority, is_active)
        # Structure: [{"condition": callable, "effect": "allow"|"deny", "priority": int}]
        self.rules: List[Dict[str, Any]] = []
    
    async def evaluate(self, request: AccessRequest) -> Optional[AccessDecision]:
        """Évaluer la requête selon les attributs."""
        logger.debug(
            "ABACPolicy evaluating",
            policy=self.name,
            requester=request.requester,
            resource=request.resource,
            action=request.action,
        )
        
        # Obtenir les attributs du demandeur
        requester_attributes = self._get_requester_attributes(request)
        resource_attributes = self._get_resource_attributes(request)
        context_attributes = request.context
        
        # Évaluer chaque règle
        for rule in sorted(self.rules, key=lambda r: r.get("priority", 0), reverse=True):
            condition = rule.get("condition")
            effect = rule.get("effect", "deny")
            
            if condition is None:
                continue
            
            try:
                # Exécuter la condition
                result = condition(
                    requester=request.requester,
                    requester_type=request.requester_type,
                    requester_attributes=requester_attributes,
                    resource=request.resource,
                    action=request.action,
                    resource_attributes=resource_attributes,
                    context=context_attributes,
                    sensitivity_level=request.sensitivity_level,
                )
                
                if result:
                    if effect == "allow":
                        logger.debug(
                            "Access GRANTED by ABAC",
                            policy=self.name,
                            rule_description=rule.get("description", "unnamed"),
                        )
                        return AccessDecision(
                            request=request,
                            allowed=True,
                            decision=DecisionType.ALLOWED,
                            reason=f"Allowed by ABAC rule: {rule.get('description', 'unnamed')}",
                            justification=request.justification,
                            policies_applied=[self.name],
                            audit_trace={
                                "policy": self.name,
                                "rule": rule.get("description", "unnamed"),
                                "decision": "allowed",
                            },
                            timestamp=datetime.utcnow(),
                        )
                    else:
                        logger.debug(
                            "Access DENIED by ABAC",
                            policy=self.name,
                            rule_description=rule.get("description", "unnamed"),
                        )
                        return AccessDecision(
                            request=request,
                            allowed=False,
                            decision=DecisionType.DENIED,
                            reason=f"Denied by ABAC rule: {rule.get('description', 'unnamed')}",
                            justification=request.justification,
                            policies_applied=[self.name],
                            audit_trace={
                                "policy": self.name,
                                "rule": rule.get("description", "unnamed"),
                                "decision": "denied",
                            },
                            timestamp=datetime.utcnow(),
                        )
            except Exception as e:
                logger.error(
                    "ABAC rule evaluation error",
                    policy=self.name,
                    error=str(e),
                )
                continue
        
        # Aucune règle ne s'applique
        return None
    
    def _get_requester_attributes(self, request: AccessRequest) -> Dict[str, Any]:
        """Obtenir les attributs du demandeur."""
        # À implémenter avec un vrai système d'attributs
        # Pour l'instant, retourner un dictionnaire vide
        return {}
    
    def _get_resource_attributes(self, request: AccessRequest) -> Dict[str, Any]:
        """Obtenir les attributs de la ressource."""
        # À implémenter avec un vrai système d'attributs
        # Pour l'instant, retourner un dictionnaire vide
        return {}
    
    def add_rule(
        self,
        condition: callable,
        effect: str = "allow",
        priority: int = 0,
        description: Optional[str] = None,
    ) -> None:
        """Ajouter une règle ABAC."""
        rule = {
            "condition": condition,
            "effect": effect,
            "priority": priority,
            "description": description,
        }
        self.rules.append(rule)
        logger.info(f"ABAC rule added: {description or 'unnamed'}")


# État du module
MODULE_STATUS = "SCAFFOLD"
