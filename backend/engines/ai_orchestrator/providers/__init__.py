"""
AI Providers
===========

Fournisseurs IA pour l'orchestrateur.
"""

from .base import BaseAIProvider
from .mistral import MistralAIProvider
from .openai import OpenAIProvider

__all__ = [
    "BaseAIProvider",
    "MistralAIProvider",
    "OpenAIProvider",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
