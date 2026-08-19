"""
Access Decision Engine Implementation
=====================================

Implémentation du moteur de décision d'accès.

Ce moteur est conçu pour être le point de contrôle centralisé pour toutes
les décisions d'accès dans le système HexLegIA.

Principe :
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

Aucun service manipulant une donnée sensible ou exécutant une action protégée
ne doit pouvoir contourner ce mécanisme.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from backend.core.logging import logger
from backend.engines.context import ContextEngine

from .models import (
    AccessDecisionRequest,
    AccessDecisionResponse,
    DecisionType,
    SensitivityLevel,
    RequesterType,
)
from .exceptions import (
    AccessDecisionError,
    AccessDeniedError,
    InsufficientContextError,
)


class AccessDecisionEngine:
    """
    Moteur de décision d'accès.
    
    Ce moteur implémente le contrôle centralisé des accès avec les éléments suivants :
    - Identité du demandeur
    - Type de demandeur
    - Ressource demandée
    - Action demandée
    - Contexte
    - Justification
    - Niveau de sensibilité
    - Décision
    - Raison de la décision
    - Trace d'audit
    
    Le moteur est conçu pour permettre ultérieurement des politiques RBAC/ABAC.
    
    État : SCAFFOLD
    """
    
    def __init__(self):
        """Initialiser le moteur de décision d'accès."""
        self.name = "AccessDecisionEngine"
        self.is_initialized = False
        self.context_engine: Optional[ContextEngine] = None
        self._policies: List[Dict[str, Any]] = []
        self._audit_log: List[Dict[str, Any]] = []
        logger.info(f"{self.name} initialized")
    
    async def initialize(self) -> None:
        """Initialiser le moteur."""
        if self.is_initialized:
            return
        
        # Obtenir le ContextEngine
        from backend.engines import get_engine
        try:
            self.context_engine = get_engine("ContextEngine")
        except ValueError:
            # Si le ContextEngine n'est pas encore initialisé, on l'initialise
            from backend.engines.context import ContextEngine
            self.context_engine = ContextEngine()
            await self.context_engine.initialize()
        
        # Initialiser les politiques par défaut
        await self._initialize_default_policies()
        
        self.is_initialized = True
        logger.info(f"{self.name} fully initialized")
    
    async def _initialize_default_policies(self) -> None:
        """Initialiser les politiques par défaut."""
        # Politique par défaut : refuser tout
        self._policies = [
            {
                "name": "default_deny",
                "description": "Politique par défaut : refuser tout",
                "type": "default",
                "priority": 0,
                "effect": "deny",
                "condition": lambda **kwargs: True,  # Toujours applicable
            },
        ]
        logger.info(f"Initialized {len(self._policies)} default policies")
    
    async def check_access(
        self,
        requester: str,
        resource: str,
        action: str,
        context: Optional[Dict[str, Any]] = None,
        requester_type: RequesterType = RequesterType.HUMAN,
        sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL,
        justification: Optional[str] = None,
    ) -> AccessDecisionResponse:
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
            AccessDecisionResponse: Décision d'accès.
        
        Raises:
            AccessDecisionError: Si une erreur se produit lors de la vérification.
        """
        # Générer un ID de requête
        request_id = str(uuid.uuid4())
        
        # Créer la requête
        request = AccessDecisionRequest(
            requester=requester,
            requester_type=requester_type,
            resource=resource,
            action=action,
            context=context or {},
            justification=justification,
            sensitivity_level=sensitivity_level,
            timestamp=datetime.utcnow(),
            request_id=request_id,
        )
        
        logger.info(
            "Access decision requested",
            request_id=request_id,
            requester=requester,
            resource=resource,
            action=action,
            requester_type=requester_type.value,
            sensitivity_level=sensitivity_level.value,
        )
        
        # Obtenir le contexte complet
        full_context = None
        if self.context_engine:
            try:
                full_context = await self.context_engine.get_context_for_decision(
                    requester_id=requester,
                    resource=resource,
                    action=action,
                    requester_type=requester_type.value,
                )
            except Exception as e:
                logger.warning(
                    "Failed to get full context",
                    error=str(e),
                    request_id=request_id,
                )
        
        # Évaluer les politiques
        decision = await self._evaluate_policies(request, full_context)
        
        # Créer la réponse
        response = AccessDecisionResponse(
            request=request,
            decision=decision["decision"],
            allowed=decision["allowed"],
            reason=decision.get("reason"),
            justification=decision.get("justification"),
            conditions=decision.get("conditions", []),
            policies_applied=decision.get("policies_applied", []),
            audit_trace={
                "engine": self.name,
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "policies_evaluated": decision.get("policies_evaluated", []),
            },
            timestamp=datetime.utcnow(),
            confidence_score=decision.get("confidence_score", 0.0),
        )
        
        # Logger la décision
        if response.allowed:
            logger.info(
                "Access GRANTED",
                request_id=request_id,
                requester=requester,
                resource=resource,
                action=action,
                reason=response.reason,
            )
        else:
            logger.warning(
                "Access DENIED",
                request_id=request_id,
                requester=requester,
                resource=resource,
                action=action,
                reason=response.reason,
            )
        
        # Enregistrer dans l'audit
        await self._log_audit(response)
        
        return response
    
    async def _evaluate_policies(
        self,
        request: AccessDecisionRequest,
        full_context: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Évaluer les politiques pour une requête.
        
        Args:
            request: La requête d'accès.
            full_context: Le contexte complet.
        
        Returns:
            Dict[str, Any]: Résultat de l'évaluation.
        """
        policies_evaluated = []
        policies_applied = []
        
        # Trier les politiques par priorité (plus élevée en premier)
        sorted_policies = sorted(self._policies, key=lambda p: p.get("priority", 0), reverse=True)
        
        for policy in sorted_policies:
            policy_name = policy.get("name", "unknown")
            policy_type = policy.get("type", "unknown")
            condition = policy.get("condition")
            effect = policy.get("effect", "deny")
            
            policies_evaluated.append(policy_name)
            
            try:
                # Vérifier si la politique s'applique
                if condition is None:
                    continue
                
                # Préparer les arguments pour la condition
                condition_args = {
                    "requester": request.requester,
                    "requester_type": request.requester_type,
                    "resource": request.resource,
                    "action": request.action,
                    "sensitivity_level": request.sensitivity_level,
                    "context": request.context,
                    "justification": request.justification,
                    "full_context": full_context,
                }
                
                # Exécuter la condition
                condition_result = condition(**condition_args)
                
                if condition_result:
                    policies_applied.append(policy_name)
                    
                    # Si c'est une politique d'autorisation, on peut retourner immédiatement
                    if effect == "allow":
                        return {
                            "decision": DecisionType.ALLOWED,
                            "allowed": True,
                            "reason": f"Allowed by policy: {policy_name}",
                            "justification": request.justification,
                            "conditions": [],
                            "policies_applied": policies_applied,
                            "policies_evaluated": policies_evaluated,
                            "confidence_score": 1.0,
                        }
                    # Si c'est une politique de refus, on continue (une politique de priorité plus élevée pourrait autoriser)
                    elif effect == "deny":
                        continue
            except Exception as e:
                logger.error(
                    "Policy evaluation error",
                    policy=policy_name,
                    error=str(e),
                )
                continue
        
        # Si aucune politique n'a autorisé l'accès, refuser par défaut
        return {
            "decision": DecisionType.DENIED,
            "allowed": False,
            "reason": "No policy allowed access - default deny",
            "justification": request.justification,
            "conditions": [],
            "policies_applied": policies_applied,
            "policies_evaluated": policies_evaluated,
            "confidence_score": 1.0,
        }
    
    async def _log_audit(self, response: AccessDecisionResponse) -> None:
        """Enregistrer une décision dans l'audit."""
        audit_entry = {
            "request_id": response.request.request_id,
            "requester": response.request.requester,
            "requester_type": response.request.requester_type.value,
            "resource": response.request.resource,
            "action": response.request.action,
            "decision": response.decision.value,
            "allowed": response.allowed,
            "reason": response.reason,
            "timestamp": response.timestamp.isoformat() + "Z",
            "metadata": {
                "policies_applied": response.policies_applied,
                "confidence_score": response.confidence_score,
            },
        }
        
        self._audit_log.append(audit_entry)
        
        # Limiter la taille du log
        if len(self._audit_log) > 1000:
            self._audit_log = self._audit_log[-1000:]
        
        logger.debug("Audit log entry created", request_id=response.request.request_id)
    
    async def add_policy(
        self,
        name: str,
        condition: callable,
        effect: str = "allow",
        priority: int = 0,
        description: Optional[str] = None,
        policy_type: str = "custom",
    ) -> None:
        """
        Ajouter une politique au moteur.
        
        Args:
            name: Nom de la politique.
            condition: Fonction condition pour la politique.
            effect: Effet de la politique ("allow" ou "deny").
            priority: Priorité de la politique.
            description: Description de la politique.
            policy_type: Type de la politique.
        """
        policy = {
            "name": name,
            "description": description,
            "type": policy_type,
            "priority": priority,
            "effect": effect,
            "condition": condition,
        }
        
        self._policies.append(policy)
        logger.info(f"Policy added: {name}")
    
    async def remove_policy(self, policy_name: str) -> bool:
        """Retirer une politique du moteur."""
        initial_count = len(self._policies)
        self._policies = [p for p in self._policies if p.get("name") != policy_name]
        
        if len(self._policies) < initial_count:
            logger.info(f"Policy removed: {policy_name}")
            return True
        return False
    
    async def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtenir les entrées d'audit."""
        return self._audit_log[-limit:]
    
    async def cleanup(self) -> None:
        """Nettoyer les ressources du moteur."""
        self._policies.clear()
        self._audit_log.clear()
        self.is_initialized = False
        logger.info(f"{self.name} cleaned up")


# État du module
MODULE_STATUS = "SCAFFOLD"
