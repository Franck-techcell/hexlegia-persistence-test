"""
AI Orchestrator Models
======================

Modèles pour l'orchestrateur IA.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class AIProviderType(str, Enum):
    """Type de fournisseur IA."""
    MISTRAL = "mistral"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    LOCAL = "local"
    CUSTOM = "custom"


class AIModelType(str, Enum):
    """Type de modèle IA."""
    TEXT = "text"
    CHAT = "chat"
    EMBEDDING = "embedding"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"


class AIRequest(BaseModel):
    """Requête IA."""
    provider_type: Optional[AIProviderType] = Field(default=None, description="Type de fournisseur (optionnel)")
    model: str = Field(..., description="Nom du modèle")
    model_type: AIModelType = Field(default=AIModelType.TEXT, description="Type de modèle")
    prompt: Optional[str] = Field(default=None, description="Prompt pour les modèles text")
    messages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Messages pour les modèles chat")
    input: Optional[Any] = Field(default=None, description="Entrée pour les autres types de modèles")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres du modèle")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte supplémentaire")
    requester: Optional[str] = Field(default=None, description="Demandeur de la requête")
    request_id: Optional[str] = Field(default=None, description="ID de la requête")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AIResponse(BaseModel):
    """Réponse IA."""
    request: AIRequest
    provider_type: AIProviderType
    model: str
    model_type: AIModelType
    output: Any = Field(..., description="Sortie du modèle")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Utilisation des tokens")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées de la réponse")
    error: Optional[str] = Field(default=None, description="Erreur éventuelle")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: float = Field(default=0.0, description="Durée de la requête en ms")


class AIProviderConfig(BaseModel):
    """Configuration d'un fournisseur IA."""
    provider_type: AIProviderType
    name: str
    description: Optional[str] = None
    api_key: Optional[str] = None
    api_url: str
    default_model: str
    available_models: List[str] = Field(default_factory=list)
    is_active: bool = True
    priority: int = 0
    timeout: float = 30.0
    max_retries: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AIProviderHealth(BaseModel):
    """Santé d'un fournisseur IA."""
    provider_type: AIProviderType
    provider_name: str
    status: str  # "healthy", "degraded", "unhealthy"
    last_check: datetime = Field(default_factory=datetime.utcnow)
    last_error: Optional[str] = None
    response_time_ms: Optional[float] = None
    available_models: List[str] = Field(default_factory=list)


class AIOrchestratorConfig(BaseModel):
    """Configuration de l'orchestrateur IA."""
    default_provider: Optional[AIProviderType] = None
    fallback_providers: List[AIProviderType] = Field(default_factory=list)
    enable_logging: bool = True
    enable_metrics: bool = True
    enable_caching: bool = False
    cache_ttl: int = 3600  # 1 heure
    max_concurrent_requests: int = 100


# État du module
MODULE_STATUS = "SCAFFOLD"
