"""
HexLegIA Engines Module
=======================

Module contenant les 14 moteurs spécialisés HexLegIA.

Chaque moteur est conçu pour être :
- Modulaire et indépendant
- Facilement extensible
- Testable individuellement
- Intégrable avec les autres composants
"""

from .verification import VerificationEngine
from .context import ContextEngine
from .access_decision import AccessDecisionEngine as AccessDecisionEngineAlias
from .ai_orchestrator import AIOrchestrator
from .simulation import SimulationEngine
from .risk import RiskEngine
from .decision import DecisionEngine
from .action import ActionEngine
from .knowledge_graph import KnowledgeGraphEngine
from .workflow import WorkflowEngine
from .collaboration import CollaborationEngine
from .notification import NotificationEngine
from .document_generator import DocumentGeneratorEngine
from .connector import ConnectorEngine

# Liste de tous les moteurs
ENGINES = [
    VerificationEngine,
    ContextEngine,
    AccessDecisionEngineAlias,
    AIOrchestrator,
    SimulationEngine,
    RiskEngine,
    DecisionEngine,
    ActionEngine,
    KnowledgeGraphEngine,
    WorkflowEngine,
    CollaborationEngine,
    NotificationEngine,
    DocumentGeneratorEngine,
    ConnectorEngine,
]

# Dictionnaire des moteurs par nom
ENGINES_BY_NAME = {engine.__name__: engine for engine in ENGINES}

# Instances des moteurs (à initialiser)
_engine_instances: dict = {}


async def init_engines() -> None:
    """Initialiser toutes les instances des moteurs."""
    from backend.core.logging import logger
    
    for engine_class in ENGINES:
        engine_name = engine_class.__name__
        try:
            # Créer l'instance
            instance = engine_class()
            _engine_instances[engine_name] = instance
            
            # Appeler la méthode d'initialisation si elle existe
            if hasattr(instance, "initialize"):
                if asyncio.iscoroutinefunction(instance.initialize):
                    await instance.initialize()
                else:
                    instance.initialize()
            
            logger.info(f"Engine initialized: {engine_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize engine: {engine_name}", error=str(e))
            raise


async def cleanup_engines() -> None:
    """Nettoyer toutes les instances des moteurs."""
    from backend.core.logging import logger
    import asyncio
    
    for engine_name, instance in _engine_instances.items():
        try:
            # Appeler la méthode de nettoyage si elle existe
            if hasattr(instance, "cleanup"):
                if asyncio.iscoroutinefunction(instance.cleanup):
                    await instance.cleanup()
                else:
                    instance.cleanup()
            
            logger.info(f"Engine cleaned up: {engine_name}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup engine: {engine_name}", error=str(e))


def get_engine(engine_name: str):
    """Obtenir une instance de moteur."""
    if engine_name not in _engine_instances:
        raise ValueError(f"Engine not initialized: {engine_name}")
    return _engine_instances[engine_name]


__all__ = [
    "VerificationEngine",
    "ContextEngine",
    "AccessDecisionEngineAlias",
    "AIOrchestrator",
    "SimulationEngine",
    "RiskEngine",
    "DecisionEngine",
    "ActionEngine",
    "KnowledgeGraphEngine",
    "WorkflowEngine",
    "CollaborationEngine",
    "NotificationEngine",
    "DocumentGeneratorEngine",
    "ConnectorEngine",
    "ENGINES",
    "ENGINES_BY_NAME",
    "init_engines",
    "cleanup_engines",
    "get_engine",
]

# État du module
MODULE_STATUS = "SCAFFOLD"
