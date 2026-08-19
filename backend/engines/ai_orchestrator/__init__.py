"""
AI Orchestrator Engine
=====================

Moteur d'orchestration des fournisseurs IA.

Rôle :
- Fournir une abstraction pour les fournisseurs IA
- Permettre l'interchangeabilité des fournisseurs
- Gérer les requêtes, réponses et erreurs
- Assurer la traçabilité des appels IA

Architecture :
    AIOrchestrator
          ↓
    AI Provider Interface
          ↓
    ┌──────────┬──────────┬──────────┐
    │ Mistral  │ OpenAI   │  Autre   │
    └──────────┴──────────┴──────────┘

État : SCAFFOLD
"""

from .engine import AIOrchestrator
from .models import (
    AIRequest,
    AIResponse,
    AIProviderConfig,
    AIProviderType,
)
from .providers import (
    BaseAIProvider,
    MistralAIProvider,
    OpenAIProvider,
)
from .exceptions import AIOrchestratorError

__all__ = [
    "AIOrchestrator",
    "AIRequest",
    "AIResponse",
    "AIProviderConfig",
    "AIProviderType",
    "BaseAIProvider",
    "MistralAIProvider",
    "OpenAIProvider",
    "AIOrchestratorError",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
