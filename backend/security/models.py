"""
Security Models
==============

Modèles de données pour la sécurité.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    """Type de demandeur."""
    HUMAN = "human"
    AI = "ai"
    SERVICE = "service"
    SYSTEM = "system"


class ResourceType(str, Enum):
    """Type de ressource."""
    DATA = "data"
    API = "api"
    DOCUMENT = "document"
    ACTION = "action"
    SYSTEM = "system"


class ActionType(str, Enum):
    """Type d'action."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"
    CREATE = "create"
    UPDATE = "update"


class SensitivityLevel(str, Enum):
    """Niveau de sensibilité."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"


class DecisionType(str, Enum):
    """Type de décision."""
    ALLOWED = "allowed"
    DENIED = "denied"
    PENDING = "pending"


# ========================================
# User Model
# ========================================

class User(BaseModel):
    """Modèle utilisateur."""
    id: Optional[str] = None
    username: str
    email: Optional[str] = None
    user_type: UserType = UserType.HUMAN
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    # Métadonnées
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ========================================
# Role Model
# ========================================

class Role(BaseModel):
    """Modèle de rôle."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    is_default: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ========================================
# Permission Model
# ========================================

class Permission(BaseModel):
    """Modèle de permission."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    resource_type: ResourceType
    action_type: ActionType
    sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL
    created_at: Optional[datetime] = None


# ========================================
# Access Request Model
# ========================================

class AccessRequest(BaseModel):
    """Modèle de requête d'accès."""
    requester: str = Field(..., description="Identité du demandeur")
    requester_type: UserType = Field(default=UserType.HUMAN, description="Type du demandeur")
    resource: str = Field(..., description="Ressource demandée")
    resource_type: Optional[ResourceType] = None
    action: str = Field(..., description="Action demandée")
    action_type: Optional[ActionType] = None
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte de la requête")
    justification: Optional[str] = None
    sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


# ========================================
# Access Decision Model
# ========================================

class AccessDecision(BaseModel):
    """Modèle de décision d'accès."""
    request: AccessRequest
    allowed: bool
    decision: DecisionType
    reason: Optional[str] = None
    justification: Optional[str] = None
    policies_applied: List[str] = Field(default_factory=list)
    audit_trace: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ========================================
# Audit Log Model
# ========================================

class AuditLog(BaseModel):
    """Modèle de log d'audit."""
    id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    requester: str
    requester_type: UserType
    resource: str
    action: str
    decision: DecisionType
    result: str
    reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ========================================
# Policy Model
# ========================================

class Policy(BaseModel):
    """Modèle de politique d'accès."""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    policy_type: str  # "rbac" ou "abac"
    rules: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# État du module
MODULE_STATUS = "SCAFFOLD"
