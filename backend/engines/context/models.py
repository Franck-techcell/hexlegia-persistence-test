"""
Context Engine Models
=====================

Modèles pour le moteur de contexte.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ContextType(str, Enum):
    """Type de contexte."""
    USER = "user"
    ORGANIZATION = "organization"
    REQUEST = "request"
    TEMPORAL = "temporal"
    REGULATORY = "regulatory"
    HISTORICAL = "historical"


class BaseContext(BaseModel):
    """Contexte de base."""
    context_type: ContextType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UserContext(BaseContext):
    """Contexte utilisateur."""
    context_type: ContextType = ContextType.USER
    
    user_id: str
    username: str
    email: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    is_authenticated: bool = False
    authentication_method: Optional[str] = None
    authentication_timestamp: Optional[datetime] = None
    
    # Attributs utilisateur
    attributes: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    # Contexte de session
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class OrganizationContext(BaseContext):
    """Contexte organisationnel."""
    context_type: ContextType = ContextType.ORGANIZATION
    
    organization_id: str
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[int] = None
    
    # Hiérarchie organisationnelle
    parent_organization_id: Optional[str] = None
    child_organizations: List[str] = Field(default_factory=list)
    
    # Politiques organisationnelles
    policies: Dict[str, Any] = Field(default_factory=dict)
    compliance_requirements: List[str] = Field(default_factory=list)
    
    # Utilisateurs de l'organisation
    user_ids: List[str] = Field(default_factory=list)


class RequestContext(BaseContext):
    """Contexte de la requête."""
    context_type: ContextType = ContextType.REQUEST
    
    request_id: str
    requester_id: str
    requester_type: str  # "user", "ai", "service", "system"
    resource: str
    action: str
    
    # Contexte HTTP
    http_method: Optional[str] = None
    http_path: Optional[str] = None
    http_query_params: Dict[str, Any] = Field(default_factory=dict)
    http_headers: Dict[str, str] = Field(default_factory=dict)
    
    # Données de la requête
    request_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Réponse attendue
    expected_response_type: Optional[str] = None


class TemporalContext(BaseContext):
    """Contexte temporel."""
    context_type: ContextType = ContextType.TEMPORAL
    
    current_time: datetime = Field(default_factory=datetime.utcnow)
    timezone: str = "UTC"
    
    # Période de validité
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    
    # Événements temporels
    events: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Planification
    schedule: Optional[Dict[str, Any]] = None


class RegulatoryContext(BaseContext):
    """Contexte réglementaire."""
    context_type: ContextType = ContextType.REGULATORY
    
    jurisdiction: str
    applicable_laws: List[str] = Field(default_factory=list)
    compliance_standards: List[str] = Field(default_factory=list)
    
    # Règles spécifiques
    data_protection_rules: Dict[str, Any] = Field(default_factory=dict)
    access_control_rules: Dict[str, Any] = Field(default_factory=dict)
    audit_requirements: Dict[str, Any] = Field(default_factory=dict)
    
    # Restrictions
    restrictions: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


class HistoricalContext(BaseContext):
    """Contexte historique."""
    context_type: ContextType = ContextType.HISTORICAL
    
    # Historique des actions
    action_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Historique des décisions
    decision_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Historique des accès
    access_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Patterns détectés
    patterns: Dict[str, Any] = Field(default_factory=dict)
    
    # Statistiques
    statistics: Dict[str, Any] = Field(default_factory=dict)


class Context(BaseContext):
    """Contexte complet."""
    user_context: Optional[UserContext] = None
    organization_context: Optional[OrganizationContext] = None
    request_context: Optional[RequestContext] = None
    temporal_context: Optional[TemporalContext] = None
    regulatory_context: Optional[RegulatoryContext] = None
    historical_context: Optional[HistoricalContext] = None
    
    # Contexte personnalisé
    custom_contexts: Dict[str, BaseContext] = Field(default_factory=dict)
    
    def get_context(self, context_type: ContextType) -> Optional[BaseContext]:
        """Obtenir un contexte spécifique."""
        context_map = {
            ContextType.USER: self.user_context,
            ContextType.ORGANIZATION: self.organization_context,
            ContextType.REQUEST: self.request_context,
            ContextType.TEMPORAL: self.temporal_context,
            ContextType.REGULATORY: self.regulatory_context,
            ContextType.HISTORICAL: self.historical_context,
        }
        return context_map.get(context_type)


# État du module
MODULE_STATUS = "SCAFFOLD"
