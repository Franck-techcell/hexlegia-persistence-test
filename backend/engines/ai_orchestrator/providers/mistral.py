"""
Mistral AI Provider
===================

Fournisseur IA pour Mistral.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import time
import httpx

from backend.core.logging import logger
from backend.core.config import settings

from .base import BaseAIProvider
from ..models import (
    AIRequest,
    AIResponse,
    AIProviderType,
    AIModelType,
    AIProviderConfig,
)
from ..exceptions import (
    AIOrchestratorError,
    AIRequestError,
    AIRequestTimeoutError,
)


class MistralAIProvider(BaseAIProvider):
    """
    Fournisseur IA pour Mistral.
    
    Ce fournisseur implémente l'interface avec l'API Mistral.
    """
    
    def __init__(self, config: Optional[AIProviderConfig] = None):
        """Initialiser le fournisseur Mistral."""
        if config is None:
            config = self._get_default_config()
        super().__init__(config)
        
        # Configuration spécifique Mistral
        self.api_key = config.api_key or settings.mistral_api_key
        self.api_url = config.api_url or settings.mistral_api_url
        
        # Client HTTP
        self.client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=config.timeout or 30.0,
        )
    
    def _get_default_config(self) -> AIProviderConfig:
        """Obtenir la configuration par défaut."""
        return AIProviderConfig(
            provider_type=AIProviderType.MISTRAL,
            name="mistral",
            description="Mistral AI Provider",
            api_key=settings.mistral_api_key,
            api_url=settings.mistral_api_url,
            default_model="mistral-tiny",
            available_models=[
                "mistral-tiny",
                "mistral-small",
                "mistral-medium",
                "mistral-large",
                "mistral-embed",
            ],
            is_active=True,
            priority=10,
            timeout=30.0,
            max_retries=3,
        )
    
    async def execute(
        self,
        request: AIRequest,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête IA avec Mistral.
        
        Args:
            request: La requête IA.
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        
        Raises:
            AIRequestError: Si la requête échoue.
            AIRequestTimeoutError: Si la requête timeout.
        """
        start_time = time.time()
        
        # Valider le modèle
        self.validate_model(request.model)
        
        # Préparer les données de la requête
        request_data = self._prepare_request_data(request)
        
        try:
            # Exécuter la requête
            response = await self.client.post(
                f"/{self._get_api_endpoint(request.model_type)}",
                json=request_data,
            )
            
            # Vérifier le statut
            response.raise_for_status()
            
            # Traiter la réponse
            response_data = response.json()
            
            # Calculer la durée
            duration_ms = (time.time() - start_time) * 1000
            
            # Créer la réponse
            ai_response = AIResponse(
                request=request,
                provider_type=AIProviderType.MISTRAL,
                model=request.model,
                model_type=request.model_type,
                output=self._extract_output(response_data, request.model_type),
                usage=self._extract_usage(response_data),
                metadata={
                    "response_id": response_data.get("id"),
                    "model": response_data.get("model"),
                },
                timestamp=datetime.utcnow(),
                duration_ms=duration_ms,
            )
            
            logger.info(
                "Mistral AI request completed",
                model=request.model,
                model_type=request.model_type.value,
                duration_ms=duration_ms,
            )
            
            return ai_response
            
        except httpx.TimeoutException as e:
            duration_ms = (time.time() - start_time) * 1000
            raise AIRequestTimeoutError(
                provider_type=AIProviderType.MISTRAL.value,
                model=request.model,
                timeout_seconds=self.config.timeout or 30.0,
            )
        except httpx.HTTPStatusError as e:
            duration_ms = (time.time() - start_time) * 1000
            raise AIRequestError(
                provider_type=AIProviderType.MISTRAL.value,
                model=request.model,
                error_message=f"HTTP {e.response.status_code}: {e.response.text}",
                error_code=str(e.response.status_code),
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            raise AIRequestError(
                provider_type=AIProviderType.MISTRAL.value,
                model=request.model,
                error_message=str(e),
            )
    
    def _prepare_request_data(self, request: AIRequest) -> Dict[str, Any]:
        """Préparer les données de la requête pour l'API Mistral."""
        if request.model_type == AIModelType.CHAT:
            return {
                "model": request.model,
                "messages": request.messages or [],
                "temperature": request.parameters.get("temperature", 0.7),
                "max_tokens": request.parameters.get("max_tokens", 1024),
                "top_p": request.parameters.get("top_p", 1.0),
            }
        elif request.model_type == AIModelType.TEXT:
            return {
                "model": request.model,
                "prompt": request.prompt or "",
                "temperature": request.parameters.get("temperature", 0.7),
                "max_tokens": request.parameters.get("max_tokens", 1024),
            }
        elif request.model_type == AIModelType.EMBEDDING:
            return {
                "model": request.model,
                "input": request.input,
            }
        else:
            return {
                "model": request.model,
                "prompt": request.prompt or request.input or "",
            }
    
    def _get_api_endpoint(self, model_type: AIModelType) -> str:
        """Obtenir le endpoint API pour le type de modèle."""
        if model_type == AIModelType.CHAT:
            return "chat/completions"
        elif model_type == AIModelType.EMBEDDING:
            return "embeddings"
        else:
            return "completions"
    
    def _extract_output(self, response_data: Dict[str, Any], model_type: AIModelType) -> Any:
        """Extraire la sortie de la réponse."""
        if model_type == AIModelType.CHAT:
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0].get("message", {}).get("content", "")
            return ""
        elif model_type == AIModelType.EMBEDDING:
            if "data" in response_data:
                return [item.get("embedding") for item in response_data["data"]]
            return []
        else:
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0].get("text", "")
            return ""
    
    def _extract_usage(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extraire les informations d'utilisation."""
        if "usage" in response_data:
            return {
                "prompt_tokens": response_data["usage"].get("prompt_tokens", 0),
                "completion_tokens": response_data["usage"].get("completion_tokens", 0),
                "total_tokens": response_data["usage"].get("total_tokens", 0),
            }
        return {}
    
    async def get_available_models(self) -> List[str]:
        """
        Obtenir la liste des modèles disponibles.
        
        Returns:
            List[str]: Liste des noms de modèles.
        """
        try:
            response = await self.client.get("/models")
            response.raise_for_status()
            data = response.json()
            
            if "data" in data:
                return [model["id"] for model in data["data"]]
            return []
            
        except Exception as e:
            logger.error(f"Failed to get Mistral models: {str(e)}")
            return self.config.available_models or []
    
    async def check_health(self) -> Dict[str, Any]:
        """
        Vérifier la santé du fournisseur.
        
        Returns:
            Dict[str, Any]: État de santé.
        """
        try:
            # Faire une requête simple pour vérifier la santé
            response = await self.client.get("/models")
            response.raise_for_status()
            
            return {
                "status": "healthy",
                "message": "API accessible",
                "response_time_ms": 0,
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": str(e),
                "response_time_ms": 0,
            }
    
    async def close(self) -> None:
        """Fermer le client HTTP."""
        await self.client.aclose()


# État du module
MODULE_STATUS = "SCAFFOLD"
