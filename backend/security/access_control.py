"""
Access Decision Engine
=====================

Moteur de décision d'accès centralisé.

Ce composant est le point de contrôle unique pour toutes les décisions d'accès.
Aucun service manipulant une donnée sensible ou exécutant une action protégée
ne doit pouvoir contourner ce mécanisme.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from backend.core.logging import logger
from backend.core.exceptions import AuthorizationError
from .models import (
    AccessRequest,
    AccessDecision,
    DecisionType,
    UserType,
    SensitivityLevel,
)
from .policies import BasePolicy, RBACPolicy, ABACPolicy


class AccessDecisionEngine:
    """
    Moteur de décision d'accès.
    
    Ce moteur implémente le pattern suivant :
    
    Utilisateur / IA
           ↓
    Authentification
           ↓
    ACCESS DECISION ENGINE
           ↓
    Autorisé ?
       ↓          ↓
      OUI         NON
       ↓           ↓
    Accès       Refus
    """
    
    def __init__(self):
        """Initialiser le moteur de décision d'accès."""
        self.policies: List[BasePolicy] = []
        self._initialize_policies()
        logger.info("AccessDecisionEngine initialized")
    
    def _initialize_policies(self) -> None:
        """Initialiser les politiques par défaut."""
        # Ajouter les politiques par défaut
        self.policies = [
            # Politique RBAC de base
            RBACPolicy(
                name="default_rbac",
                description="Politique RBAC par défaut",
                priority=10,
            ),
            # Politique ABAC de base
            ABACPolicy(
                name="default_abac",
                description="Politique ABAC par défaut",
                priority=20,
            ),
        ]
        logger.info(f"Initialized {len(self.policies)} policies")
    
    async def check_access(
        self,
        requester: str,
        resource: str,
        action: str,
        context: Optional[Dict[str, Any]] = None,
        requester_type: UserType = UserType.HUMAN,
        sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL,
        justification: Optional[str] = None,
    ) -> AccessDecision:
        """
        Vérifier l'accès à une ressource.
        
        Args:
            requester: Identité du demandeur.
            resource: Ressource demandée.
            action: Action demandée.
            context: Contexte supplémentaire.
            requester_type: Type du demandeur.
            sensitivity_level: Niveau de sensibilité.
            justification: Justification de la requête.
        
        Returns:
            AccessDecision: Décision d'accès.
        
        Raises:
            AuthorizationError: Si une erreur se produit lors de la vérification.
        """
        # Créer la requête d'accès
        request = AccessRequest(
            requester=requester,
            requester_type=requester_type,
            resource=resource,
            action=action,
            context=context or {},
            justification=justification,
            sensitivity_level=sensitivity_level,
            timestamp=datetime.utcnow(),
        )
        
        logger.info(
            "Access check requested",
            requester=requester,
            resource=resource,
            action=action,
            requester_type=requester_type.value,
            sensitivity_level=sensitivity_level.value,
        )
        
        # Appliquer les politiques dans l'ordre de priorité
        decision = None
        for policy in sorted(self.policies, key=lambda p: p.priority):
            if not policy.is_active:
                continue
                
            policy_decision = await policy.evaluate(request)
            
            if policy_decision is not None:
                decision = policy_decision
                
                # Si la décision est DENIED, on peut s'arrêter (sauf si une politique
                # de priorité plus élevée peut l'outrepasser)
                if policy_decision.decision == DecisionType.DENIED:
                    # Vérifier si une politique de priorité plus élevée peut autoriser
                    for higher_policy in self.policies:
                        if higher_policy.priority > policy.priority and higher_policy.is_active:
                            higher_decision = await higher_policy.evaluate(request)
                            if higher_decision and higher_decision.decision == DecisionType.ALLOWED:
                                decision = higher_decision
                                break
                    break
        
        # Si aucune politique n'a retourné de décision, refuser par défaut
        if decision is None:
            decision = AccessDecision(
                request=request,
                allowed=False,
                decision=DecisionType.DENIED,
                reason="No policy matched - default deny",
                justification=None,
                policies_applied=[],
                audit_trace={"default_decision": True},
                timestamp=datetime.utcnow(),
            )
        
        # Ajouter les informations de trace
        decision.audit_trace["engine"] = "AccessDecisionEngine"
        decision.audit_trace["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        # Logger la décision
        if decision.allowed:
            logger.info(
                "Access GRANTED",
                requester=requester,
                resource=resource,
                action=action,
                reason=decision.reason,
            )
        else:
            logger.warning(
                "Access DENIED",
                requester=requester,
                resource=resource,
                action=action,
                reason=decision.reason,
            )
        
        return decision
    
    async def check_access_with_justification(
        self,
        requester: str,
        resource: str,
        action: str,
        justification: str,
        context: Optional[Dict[str, Any]] = None,
        requester_type: UserType = UserType.HUMAN,
        sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL,
    ) -> AccessDecision:
        """
        Vérifier l'accès avec justification obligatoire.
        
        Args:
            requester: Identité du demandeur.
            resource: Ressource demandée.
            action: Action demandée.
            justification: Justification obligatoire.
            context: Contexte supplémentaire.
            requester_type: Type du demandeur.
            sensitivity_level: Niveau de sensibilité.
        
        Returns:
            AccessDecision: Décision d'accès.
        """
        if not justification:
            raise AuthorizationError(
                message="Justification is required for this access request",
                details={
                    "requester": requester,
                    "resource": resource,
                    "action": action,
                },
            )
        
        return await self.check_access(
            requester=requester,
            resource=resource,
            action=action,
            context=context,
            requester_type=requester_type,
            sensitivity_level=sensitivity_level,
            justification=justification,
        )
    
    def add_policy(self, policy: BasePolicy) -> None:
        """Ajouter une politique au moteur."""
        self.policies.append(policy)
        # Réorganiser par priorité
        self.policies.sort(key=lambda p: p.priority)
        logger.info(f"Policy added: {policy.name}")
    
    def remove_policy(self, policy_name: str) -> bool:
        """Retirer une politique du moteur."""
        initial_count = len(self.policies)
        self.policies = [p for p in self.policies if p.name != policy_name]
        
        if len(self.policies) < initial_count:
            logger.info(f"Policy removed: {policy_name}")
            return True
        return False
    
    def get_policy(self, policy_name: str) -> Optional[BasePolicy]:
        """Obtenir une politique par son nom."""
        for policy in self.policies:
            if policy.name == policy_name:
                return policy
        return None


# État du module
MODULE_STATUS = "SCAFFOLD"
