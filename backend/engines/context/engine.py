"""
Context Engine Implementation
=============================

Implémentation du moteur de contexte.

Ce moteur centralise toutes les informations de contexte nécessaires
pour les décisions, les vérifications et les opérations.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import copy

from backend.core.logging import logger

from .models import (
    Context,
    UserContext,
    OrganizationContext,
    RequestContext,
    TemporalContext,
    RegulatoryContext,
    HistoricalContext,
    ContextType,
)
from .exceptions import (
    ContextError,
    ContextNotFoundError,
)


class ContextEngine:
    """
    Moteur de gestion du contexte.
    
    Ce moteur permet de centraliser :
    - Le contexte utilisateur
    - Le contexte organisationnel
    - Les rôles et permissions
    - Les données pertinentes
    - Le contexte de la demande
    - Le contexte temporel
    - Le contexte réglementaire
    - L'historique nécessaire à la décision
    
    État : SCAFFOLD
    """
    
    def __init__(self):
        """Initialiser le moteur de contexte."""
        self.name = "ContextEngine"
        self.is_initialized = False
        
        # Stockage des contextes
        self._user_contexts: Dict[str, UserContext] = {}
        self._organization_contexts: Dict[str, OrganizationContext] = {}
        self._request_contexts: Dict[str, RequestContext] = {}
        self._temporal_contexts: Dict[str, TemporalContext] = {}
        self._regulatory_contexts: Dict[str, RegulatoryContext] = {}
        self._historical_contexts: Dict[str, HistoricalContext] = {}
        
        logger.info(f"{self.name} initialized")
    
    async def initialize(self) -> None:
        """Initialiser le moteur."""
        if self.is_initialized:
            return
        
        # Initialiser les contextes par défaut
        await self._initialize_default_contexts()
        
        self.is_initialized = True
        logger.info(f"{self.name} fully initialized")
    
    async def _initialize_default_contexts(self) -> None:
        """Initialiser les contextes par défaut."""
        # Créer un contexte temporel par défaut
        default_temporal = TemporalContext(
            current_time=datetime.utcnow(),
            timezone="UTC",
        )
        self._temporal_contexts["default"] = default_temporal
        
        # Créer un contexte réglementaire par défaut
        default_regulatory = RegulatoryContext(
            jurisdiction="global",
            applicable_laws=["GDPR", "ISO_27001"],
            compliance_standards=["SOC2", "PCI_DSS"],
        )
        self._regulatory_contexts["default"] = default_regulatory
        
        logger.info("Default contexts initialized")
    
    # ========================================
    # User Context Methods
    # ========================================
    
    async def create_user_context(
        self,
        user_id: str,
        username: str,
        email: Optional[str] = None,
        roles: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        is_authenticated: bool = False,
        authentication_method: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> UserContext:
        """Créer un contexte utilisateur."""
        context = UserContext(
            user_id=user_id,
            username=username,
            email=email,
            roles=roles or [],
            permissions=permissions or [],
            is_authenticated=is_authenticated,
            authentication_method=authentication_method,
            authentication_timestamp=datetime.utcnow() if is_authenticated else None,
            attributes=attributes or {},
            preferences=preferences or {},
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        self._user_contexts[user_id] = context
        logger.info(f"User context created: {user_id}")
        
        return context
    
    async def get_user_context(self, user_id: str) -> Optional[UserContext]:
        """Obtenir un contexte utilisateur."""
        if user_id not in self._user_contexts:
            logger.warning(f"User context not found: {user_id}")
            return None
        
        return self._user_contexts[user_id]
    
    async def update_user_context(
        self,
        user_id: str,
        **kwargs,
    ) -> Optional[UserContext]:
        """Mettre à jour un contexte utilisateur."""
        context = await self.get_user_context(user_id)
        
        if context is None:
            raise ContextNotFoundError(
                context_type="user",
                context_id=user_id,
            )
        
        # Mettre à jour les champs
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
        
        context.updated_at = datetime.utcnow()
        logger.info(f"User context updated: {user_id}")
        
        return context
    
    async def delete_user_context(self, user_id: str) -> bool:
        """Supprimer un contexte utilisateur."""
        if user_id in self._user_contexts:
            del self._user_contexts[user_id]
            logger.info(f"User context deleted: {user_id}")
            return True
        return False
    
    # ========================================
    # Organization Context Methods
    # ========================================
    
    async def create_organization_context(
        self,
        organization_id: str,
        name: str,
        domain: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[int] = None,
        parent_organization_id: Optional[str] = None,
        policies: Optional[Dict[str, Any]] = None,
        compliance_requirements: Optional[List[str]] = None,
        user_ids: Optional[List[str]] = None,
    ) -> OrganizationContext:
        """Créer un contexte organisationnel."""
        context = OrganizationContext(
            organization_id=organization_id,
            name=name,
            domain=domain,
            industry=industry,
            size=size,
            parent_organization_id=parent_organization_id,
            policies=policies or {},
            compliance_requirements=compliance_requirements or [],
            user_ids=user_ids or [],
        )
        
        self._organization_contexts[organization_id] = context
        logger.info(f"Organization context created: {organization_id}")
        
        return context
    
    async def get_organization_context(self, organization_id: str) -> Optional[OrganizationContext]:
        """Obtenir un contexte organisationnel."""
        if organization_id not in self._organization_contexts:
            logger.warning(f"Organization context not found: {organization_id}")
            return None
        
        return self._organization_contexts[organization_id]
    
    # ========================================
    # Request Context Methods
    # ========================================
    
    async def create_request_context(
        self,
        request_id: str,
        requester_id: str,
        requester_type: str,
        resource: str,
        action: str,
        http_method: Optional[str] = None,
        http_path: Optional[str] = None,
        http_query_params: Optional[Dict[str, Any]] = None,
        http_headers: Optional[Dict[str, str]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        expected_response_type: Optional[str] = None,
    ) -> RequestContext:
        """Créer un contexte de requête."""
        context = RequestContext(
            request_id=request_id,
            requester_id=requester_id,
            requester_type=requester_type,
            resource=resource,
            action=action,
            http_method=http_method,
            http_path=http_path,
            http_query_params=http_query_params or {},
            http_headers=http_headers or {},
            request_data=request_data or {},
            expected_response_type=expected_response_type,
        )
        
        self._request_contexts[request_id] = context
        logger.info(f"Request context created: {request_id}")
        
        return context
    
    async def get_request_context(self, request_id: str) -> Optional[RequestContext]:
        """Obtenir un contexte de requête."""
        if request_id not in self._request_contexts:
            logger.warning(f"Request context not found: {request_id}")
            return None
        
        return self._request_contexts[request_id]
    
    # ========================================
    # Temporal Context Methods
    # ========================================
    
    async def get_temporal_context(self, context_id: str = "default") -> Optional[TemporalContext]:
        """Obtenir un contexte temporel."""
        if context_id not in self._temporal_contexts:
            logger.warning(f"Temporal context not found: {context_id}")
            return None
        
        return self._temporal_contexts[context_id]
    
    async def update_temporal_context(
        self,
        context_id: str = "default",
        **kwargs,
    ) -> Optional[TemporalContext]:
        """Mettre à jour un contexte temporel."""
        context = await self.get_temporal_context(context_id)
        
        if context is None:
            raise ContextNotFoundError(
                context_type="temporal",
                context_id=context_id,
            )
        
        # Mettre à jour les champs
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
        
        context.updated_at = datetime.utcnow()
        logger.info(f"Temporal context updated: {context_id}")
        
        return context
    
    # ========================================
    # Regulatory Context Methods
    # ========================================
    
    async def get_regulatory_context(self, context_id: str = "default") -> Optional[RegulatoryContext]:
        """Obtenir un contexte réglementaire."""
        if context_id not in self._regulatory_contexts:
            logger.warning(f"Regulatory context not found: {context_id}")
            return None
        
        return self._regulatory_contexts[context_id]
    
    # ========================================
    # Full Context Assembly
    # ========================================
    
    async def get_full_context(
        self,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        request_id: Optional[str] = None,
        temporal_context_id: str = "default",
        regulatory_context_id: str = "default",
    ) -> Context:
        """
        Assembler un contexte complet à partir des différents contextes.
        
        Args:
            user_id: ID de l'utilisateur.
            organization_id: ID de l'organisation.
            request_id: ID de la requête.
            temporal_context_id: ID du contexte temporel.
            regulatory_context_id: ID du contexte réglementaire.
        
        Returns:
            Context: Contexte complet.
        """
        # Obtenir les contextes individuels
        user_context = None
        if user_id:
            user_context = await self.get_user_context(user_id)
        
        organization_context = None
        if organization_id:
            organization_context = await self.get_organization_context(organization_id)
        
        request_context = None
        if request_id:
            request_context = await self.get_request_context(request_id)
        
        temporal_context = await self.get_temporal_context(temporal_context_id)
        regulatory_context = await self.get_regulatory_context(regulatory_context_id)
        
        # Créer le contexte complet
        full_context = Context(
            user_context=user_context,
            organization_context=organization_context,
            request_context=request_context,
            temporal_context=temporal_context,
            regulatory_context=regulatory_context,
        )
        
        logger.info(
            "Full context assembled",
            user_id=user_id,
            organization_id=organization_id,
            request_id=request_id,
        )
        
        return full_context
    
    async def get_context_for_decision(
        self,
        requester_id: str,
        resource: str,
        action: str,
        requester_type: str = "user",
        organization_id: Optional[str] = None,
    ) -> Context:
        """
        Obtenir le contexte nécessaire pour une décision d'accès.
        
        Args:
            requester_id: ID du demandeur.
            resource: Ressource demandée.
            action: Action demandée.
            requester_type: Type du demandeur.
            organization_id: ID de l'organisation.
        
        Returns:
            Context: Contexte pour la décision.
        """
        # Créer un contexte de requête
        request_id = f"req_{requester_id}_{resource}_{action}_{datetime.utcnow().timestamp()}"
        request_context = await self.create_request_context(
            request_id=request_id,
            requester_id=requester_id,
            requester_type=requester_type,
            resource=resource,
            action=action,
        )
        
        # Obtenir le contexte complet
        full_context = await self.get_full_context(
            user_id=requester_id if requester_type == "user" else None,
            organization_id=organization_id,
            request_id=request_id,
        )
        
        return full_context
    
    async def cleanup(self) -> None:
        """Nettoyer les ressources du moteur."""
        self._user_contexts.clear()
        self._organization_contexts.clear()
        self._request_contexts.clear()
        self._temporal_contexts.clear()
        self._regulatory_contexts.clear()
        self._historical_contexts.clear()
        self.is_initialized = False
        logger.info(f"{self.name} cleaned up")


# État du module
MODULE_STATUS = "SCAFFOLD"
