"""
Base AI Provider
===============

Classe de base pour les fournisseurs IA.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
import time

from backend.core.logging import logger
from backend.core.config import settings

from ..models import (
    AIRequest,
    AIResponse,
    AIProviderType,
    AIModelType,
    AIProviderConfig,
)
from ..exceptions import (
    AIOrchestratorError,
    ProviderNotConfiguredError,
    ModelNotAvailableError,
)


class BaseAIProvider(ABC):
    """
    Classe de base pour les fournisseurs IA.
    
    Chaque fournisseur IA doit implémenter cette classe et fournir :
    - Une méthode pour exécuter des requêtes
    - Une méthode pour vérifier la santé
    - Une méthode pour lister les modèles disponibles
    """
    
    def __init__(self, config: Optional[AIProviderConfig] = None):
        """
        Initialiser le fournisseur IA.
        
        Args:
            config: Configuration du fournisseur.
        """
        self.config = config or self._get_default_config()
        self.provider_type = self.config.provider_type
        self.name = self.config.name
        self.is_healthy = False
        self.last_health_check = None
        self.available_models = []
        
        # Vérifier la configuration
        self._validate_config()
        
        logger.info(f"AI Provider initialized: {self.name} ({self.provider_type.value})")
    
    @abstractmethod
    def _get_default_config(self) -> AIProviderConfig:
        """Obtenir la configuration par défaut."""
        pass
    
    def _validate_config(self) -> None:
        """Valider la configuration."""
        if not self.config:
            raise ProviderNotConfiguredError(
                provider_type=self.provider_type.value,
                message="No configuration provided",
            )
        
        if not self.config.api_url:
            raise ProviderNotConfiguredError(
                provider_type=self.provider_type.value,
                message="API URL not configured",
            )
    
    @abstractmethod
    async def execute(
        self,
        request: AIRequest,
        **kwargs,
    ) -> AIResponse:
        """
        Exécuter une requête IA.
        
        Args:
            request: La requête IA.
            **kwargs: Arguments supplémentaires.
        
        Returns:
            AIResponse: La réponse IA.
        
        Raises:
            AIOrchestratorError: Si une erreur se produit.
        """
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """
        Obtenir la liste des modèles disponibles.
        
        Returns:
            List[str]: Liste des noms de modèles.
        """
        pass
    
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """
        Vérifier la santé du fournisseur.
        
        Returns:
            Dict[str, Any]: État de santé.
        """
        pass
    
    async def refresh_available_models(self) -> None:
        """Rafraîchir la liste des modèles disponibles."""
        try:
            self.available_models = await self.get_available_models()
            logger.info(f"Refreshed available models for {self.name}: {len(self.available_models)} models")
        except Exception as e:
            logger.error(f"Failed to refresh models for {self.name}: {str(e)}")
            self.available_models = []
    
    async def health_check(self) -> bool:
        """
        Effectuer une vérification de santé complète.
        
        Returns:
            bool: True si le fournisseur est en bonne santé.
        """
        try:
            health = await self.check_health()
            self.is_healthy = health.get("status") == "healthy"
            self.last_health_check = datetime.utcnow()
            
            if self.is_healthy:
                logger.info(f"Health check passed for {self.name}")
            else:
                logger.warning(f"Health check failed for {self.name}: {health.get('message')}")
            
            return self.is_healthy
            
        except Exception as e:
            self.is_healthy = False
            self.last_health_check = datetime.utcnow()
            logger.error(f"Health check error for {self.name}: {str(e)}")
            return False
    
    def validate_model(self, model: str) -> bool:
        """
        Valider qu'un modèle est disponible.
        
        Args:
            model: Nom du modèle.
        
        Returns:
            bool: True si le modèle est disponible.
        
        Raises:
            ModelNotAvailableError: Si le modèle n'est pas disponible.
        """
        if not self.available_models:
            # Si on n'a pas encore chargé les modèles, on les charge
            import asyncio
            asyncio.run(self.refresh_available_models())
        
        if model not in self.available_models:
            raise ModelNotAvailableError(
                provider_type=self.provider_type.value,
                model=model,
                available_models=self.available_models,
            )
        
        return True
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, type={self.provider_type.value}, healthy={self.is_healthy})"


# État du module
MODULE_STATUS = "SCAFFOLD"
