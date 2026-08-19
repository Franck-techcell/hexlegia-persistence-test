"""
AI Orchestrator Implementation
==============================

Implémentation de l'orchestrateur IA.

Cet orchestrateur fournit une abstraction pour les fournisseurs IA,
permettant de changer facilement de fournisseur sans modifier le code
qui utilise l'IA.

Architecture :
    AIOrchestrator
          ↓
    AI Provider Interface
          ↓
    ┌──────────┬──────────┬──────────┐
    │ Mistral  │ OpenAI   │  Autre   │
    └──────────┴──────────┴──────────┘

Les moteurs ne doivent pas appeler directement un fournisseur IA.
Le fournisseur doit être interchangeable.
"""

from typing import Optional, Dict, Any, List, Type
from datetime import datetime
import time
import asyncio

from backend.core.logging import logger
from backend.core.config import settings

from .models import (
    AIRequest,
    AIResponse,
    AIProviderType,
    AIModelType,
    AIProviderConfig,
    AIOrchestratorConfig,
)
from .providers.base import BaseAIProvider
from .providers.mistral import MistralAIProvider
from .providers.openai import OpenAIProvider
from .exceptions import (
    AIOrchestratorError,
    NoProviderAvailableError,
    ProviderNotConfiguredError,
    ModelNotAvailableError,
)


class AIOrchestrator:
    """
    Orchestrateur IA.
    
    Ce moteur permet de :
    - Appeler différents fournisseurs IA de manière unifiée
    - Gérer les erreurs et les timeouts
    - Assurer la traçabilité des appels
    - Permettre le fallback entre fournisseurs
    
    Prévoir :
    - requête
    - contexte
    - modèle
    - paramètres
    - réponse
    - erreurs
    - métadonnées
    - traçabilité
    
    État : SCAFFOLD
    """
    
    def __init__(self, config: Optional[AIOrchestratorConfig] = None):
        """Initialiser l'orchestrateur IA."""
        self.name = "AIOrchestrator"
        self.is_initialized = False
        self.config = config or AIOrchestratorConfig()
        
        # Fournisseurs disponibles
        self.providers: Dict[AIProviderType, BaseAIProvider] = {}
        self._provider_instances: Dict[str, BaseAIProvider] = {}
        
        # Métriques
        self._metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "requests_by_provider": {},
            "requests_by_model": {},
        }
        
        logger.info(f"{self.name} initialized")
    
    async def initialize(self) -> None:
        """Initialiser l'orchestrateur."""
        if self.is_initialized:
            return
        
        # Initialiser les fournisseurs par défaut
        await self._initialize_default_providers()
        
        # Rafraîchir les modèles disponibles
        await self._refresh_provider_models()
        
        self.is_initialized = True
        logger.info(f"{self.name} fully initialized")
    
    async def _initialize_default_providers(self) -> None:
        """Initialiser les fournisseurs par défaut."""
        # Mistral
        if settings.mistral_api_key:
            mistral_config = AIProviderConfig(
                provider_type=AIProviderType.MISTRAL,
                name="mistral",
                description="Mistral AI Provider",
                api_key=settings.mistral_api_key,
                api_url=settings.mistral_api_url,
                default_model="mistral-tiny",
                is_active=True,
                priority=10,
            )
            self.register_provider(AIProviderType.MISTRAL, MistralAIProvider(mistral_config))
            logger.info("Mistral AI provider registered")
        
        # OpenAI
        if settings.openai_api_key:
            openai_config = AIProviderConfig(
                provider_type=AIProviderType.OPENAI,
                name="openai",
                description="OpenAI Provider",
                api_key=settings.openai_api_key,
                api_url=settings.openai_api_url,
                default_model="gpt-3.5-turbo",
                is_active=True,
                priority=10,
            )
            self.register_provider(AIProviderType.OPENAI, OpenAIProvider(openai_config))
            logger.info("OpenAI provider registered")
        
        if not self.providers:
            logger.warning("No AI providers configured - AI functionality will be limited")
    
    async def _refresh_provider_models(self) -> None:
        """Rafraîchir les modèles disponibles pour tous les fournisseurs."""
        for provider_type, provider in self.providers.items():
            try:
                await provider.refresh_available_models()
            except Exception as e:
                logger.error(f"Failed to refresh models for {provider.name}: {str(e)}")
    
    def register_provider(
        self,
        provider_type: AIProviderType,
        provider: BaseAIProvider,
    ) -> None:
        """
        Enregistrer un fournisseur IA.
        
        Args:
            provider_type: Type du fournisseur.
            provider: Instance du fournisseur.
        """
        self.providers[provider_type] = provider
        self._provider_instances[provider.name] = provider
        logger.info(f"Provider registered: {provider.name} ({provider_type.value})")
    
    def unregister_provider(self, provider_type: AIProviderType) -> bool:
        """
        Désenregistrer un fournisseur IA.
        
        Args:
            provider_type: Type du fournisseur.
        
        Returns:
            bool: True si le fournisseur a été désenregistré.
        """
        if provider_type in self.providers:
            provider = self.providers[provider_type]
            del self.providers[provider_type]
            if provider.name in self._provider_instances:
                del self._provider_instances[provider.name]
            logger.info(f"Provider unregistered: {provider.name}")
            return True
        return False
    
    async def execute(
        self,
        request: AIRequest,
        provider_type: Optional[AIProviderType] = None,
        fallback_enabled: bool = True,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête IA.
        
        Args:
            request: La requête IA.
            provider_type: Type de fournisseur spécifique (optionnel).
            fallback_enabled: Si True, essayer les autres fournisseurs en cas d'échec.
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        
        Raises:
            NoProviderAvailableError: Si aucun fournisseur n'est disponible.
            AIOrchestratorError: Si une erreur se produit.
        """
        start_time = time.time()
        self._metrics["total_requests"] += 1
        
        # Déterminer le fournisseur à utiliser
        if provider_type:
            providers_to_try = [self.providers.get(provider_type)]
        else:
            # Utiliser le fournisseur par défaut ou tous les fournisseurs
            if self.config.default_provider:
                providers_to_try = [self.providers.get(self.config.default_provider)]
            else:
                providers_to_try = list(self.providers.values())
        
        # Filtrer les fournisseurs valides
        providers_to_try = [p for p in providers_to_try if p is not None and p.is_healthy]
        
        if not providers_to_try:
            raise NoProviderAvailableError(
                requested_provider=provider_type.value if provider_type else "default",
                available_providers=[p.value for p in self.providers.keys()],
            )
        
        # Essayer les fournisseurs dans l'ordre
        last_error = None
        for provider in providers_to_try:
            try:
                # Exécuter la requête
                response = await provider.execute(request, **kwargs)
                
                # Mettre à jour les métriques
                self._metrics["successful_requests"] += 1
                provider_name = provider.name
                model = request.model
                
                self._metrics["requests_by_provider"][provider_name] = \
                    self._metrics["requests_by_provider"].get(provider_name, 0) + 1
                self._metrics["requests_by_model"][model] = \
                    self._metrics["requests_by_model"].get(model, 0) + 1
                
                # Ajouter des métadonnées d'orchestration
                response.metadata["orchestrator"] = {
                    "provider": provider_name,
                    "provider_type": provider.provider_type.value,
                    "fallback_used": False,
                }
                
                logger.info(
                    "AI request completed",
                    provider=provider_name,
                    model=request.model,
                    model_type=request.model_type.value,
                    duration_ms=response.duration_ms,
                )
                
                return response
                
            except Exception as e:
                last_error = e
                self._metrics["failed_requests"] += 1
                
                logger.warning(
                    "AI request failed",
                    provider=provider.name,
                    model=request.model,
                    error=str(e),
                )
                
                # Si fallback est désactivé, lever l'erreur
                if not fallback_enabled:
                    raise
                
                # Continuer avec le prochain fournisseur
                continue
        
        # Si on arrive ici, tous les fournisseurs ont échoué
        if last_error:
            raise last_error
        
        raise AIOrchestratorError(
            message="All providers failed",
            provider_type="all",
            model=request.model,
        )
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        provider_type: Optional[AIProviderType] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête de chat.
        
        Args:
            model: Modèle à utiliser.
            messages: Messages du chat.
            provider_type: Type de fournisseur (optionnel).
            temperature: Température du modèle.
            max_tokens: Nombre maximum de tokens.
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        """
        request = AIRequest(
            model=model,
            model_type=AIModelType.CHAT,
            messages=messages,
            parameters={
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs,
            },
        )
        
        return await self.execute(request, provider_type=provider_type)
    
    async def complete(
        self,
        model: str,
        prompt: str,
        provider_type: Optional[AIProviderType] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête de complétion de texte.
        
        Args:
            model: Modèle à utiliser.
            prompt: Prompt de texte.
            provider_type: Type de fournisseur (optionnel).
            temperature: Température du modèle.
            max_tokens: Nombre maximum de tokens.
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        """
        request = AIRequest(
            model=model,
            model_type=AIModelType.TEXT,
            prompt=prompt,
            parameters={
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs,
            },
        )
        
        return await self.execute(request, provider_type=provider_type)
    
    async def embed(
        self,
        model: str,
        input: Any,
        provider_type: Optional[AIProviderType] = None,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête d'embedding.
        
        Args:
            model: Modèle à utiliser.
            input: Texte ou données à embedder.
            provider_type: Type de fournisseur (optionnel).
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        """
        request = AIRequest(
            model=model,
            model_type=AIModelType.EMBEDDING,
            input=input,
            parameters=kwargs,
        )
        
        return await self.execute(request, provider_type=provider_type)
    
    async def get_available_providers(self) -> List[Dict[str, Any]]:
        """
        Obtenir la liste des fournisseurs disponibles.
        
        Returns:
            List[Dict[str, Any]]: Liste des fournisseurs avec leurs informations.
        """
        providers = []
        for provider_type, provider in self.providers.items():
            providers.append({
                "type": provider_type.value,
                "name": provider.name,
                "description": provider.config.description,
                "is_healthy": provider.is_healthy,
                "default_model": provider.config.default_model,
                "available_models": provider.available_models,
            })
        return providers
    
    async def get_available_models(
        self,
        provider_type: Optional[AIProviderType] = None,
    ) -> List[str]:
        """
        Obtenir la liste des modèles disponibles.
        
        Args:
            provider_type: Type de fournisseur (optionnel).
        
        Returns:
            List[str]: Liste des modèles disponibles.
        """
        if provider_type:
            provider = self.providers.get(provider_type)
            if provider:
                return provider.available_models
            return []
        
        # Retourner tous les modèles de tous les fournisseurs
        all_models = []
        for provider in self.providers.values():
            all_models.extend(provider.available_models)
        return list(set(all_models))
    
    async def check_health(self) -> Dict[str, Any]:
        """
        Vérifier la santé de tous les fournisseurs.
        
        Returns:
            Dict[str, Any]: État de santé global.
        """
        results = {}
        for provider_type, provider in self.providers.items():
            try:
                is_healthy = await provider.health_check()
                results[provider_type.value] = {
                    "healthy": is_healthy,
                    "provider": provider.name,
                }
            except Exception as e:
                results[provider_type.value] = {
                    "healthy": False,
                    "provider": provider.name,
                    "error": str(e),
                }
        
        return {
            "status": "healthy" if all(r["healthy"] for r in results.values()) else "degraded",
            "providers": results,
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """
        Obtenir les métriques de l'orchestrateur.
        
        Returns:
            Dict[str, Any]: Métriques de l'orchestrateur.
        """
        return {
            **self._metrics,
            "providers": {
                name: {
                    "is_healthy": provider.is_healthy,
                    "available_models": len(provider.available_models),
                }
                for name, provider in self._provider_instances.items()
            },
        }
    
    async def cleanup(self) -> None:
        """Nettoyer les ressources de l'orchestrateur."""
        for provider in self.providers.values():
            if hasattr(provider, "close"):
                try:
                    await provider.close()
                except Exception as e:
                    logger.error(f"Failed to close provider {provider.name}: {str(e)}")
        
        self.providers.clear()
        self._provider_instances.clear()
        self.is_initialized = False
        logger.info(f"{self.name} cleaned up")


# État du module
MODULE_STATUS = "SCAFFOLD"
