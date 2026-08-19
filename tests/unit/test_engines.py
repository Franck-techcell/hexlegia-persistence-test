"""
Engines Tests
============

Tests pour les 14 moteurs HexLegIA.
"""

import pytest
from backend.engines import (
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
)


class TestEnginesInitialization:
    """Tests pour l'initialisation des moteurs."""
    
    def test_verification_engine_initialization(self):
        """Tester l'initialisation du VerificationEngine."""
        engine = VerificationEngine()
        assert engine.name == "VerificationEngine"
        assert engine.is_initialized == False
    
    def test_context_engine_initialization(self):
        """Tester l'initialisation du ContextEngine."""
        engine = ContextEngine()
        assert engine.name == "ContextEngine"
        assert engine.is_initialized == False
    
    def test_access_decision_engine_initialization(self):
        """Tester l'initialisation du AccessDecisionEngine."""
        engine = AccessDecisionEngineAlias()
        assert engine.name == "AccessDecisionEngine"
        assert engine.is_initialized == False
    
    def test_ai_orchestrator_initialization(self):
        """Tester l'initialisation de l'AIOrchestrator."""
        engine = AIOrchestrator()
        assert engine.name == "AIOrchestrator"
        assert engine.is_initialized == False
    
    def test_simulation_engine_initialization(self):
        """Tester l'initialisation du SimulationEngine."""
        engine = SimulationEngine()
        assert engine.name == "SimulationEngine"
        assert engine.is_initialized == False
    
    def test_risk_engine_initialization(self):
        """Tester l'initialisation du RiskEngine."""
        engine = RiskEngine()
        assert engine.name == "RiskEngine"
        assert engine.is_initialized == False
    
    def test_decision_engine_initialization(self):
        """Tester l'initialisation du DecisionEngine."""
        engine = DecisionEngine()
        assert engine.name == "DecisionEngine"
        assert engine.is_initialized == False
    
    def test_action_engine_initialization(self):
        """Tester l'initialisation du ActionEngine."""
        engine = ActionEngine()
        assert engine.name == "ActionEngine"
        assert engine.is_initialized == False
    
    def test_knowledge_graph_engine_initialization(self):
        """Tester l'initialisation du KnowledgeGraphEngine."""
        engine = KnowledgeGraphEngine()
        assert engine.name == "KnowledgeGraphEngine"
        assert engine.is_initialized == False
    
    def test_workflow_engine_initialization(self):
        """Tester l'initialisation du WorkflowEngine."""
        engine = WorkflowEngine()
        assert engine.name == "WorkflowEngine"
        assert engine.is_initialized == False
    
    def test_collaboration_engine_initialization(self):
        """Tester l'initialisation du CollaborationEngine."""
        engine = CollaborationEngine()
        assert engine.name == "CollaborationEngine"
        assert engine.is_initialized == False
    
    def test_notification_engine_initialization(self):
        """Tester l'initialisation du NotificationEngine."""
        engine = NotificationEngine()
        assert engine.name == "NotificationEngine"
        assert engine.is_initialized == False
    
    def test_document_generator_engine_initialization(self):
        """Tester l'initialisation du DocumentGeneratorEngine."""
        engine = DocumentGeneratorEngine()
        assert engine.name == "DocumentGeneratorEngine"
        assert engine.is_initialized == False
    
    def test_connector_engine_initialization(self):
        """Tester l'initialisation du ConnectorEngine."""
        engine = ConnectorEngine()
        assert engine.name == "ConnectorEngine"
        assert engine.is_initialized == False


class TestEnginesList:
    """Tests pour la liste des moteurs."""
    
    def test_all_engines_in_list(self):
        """Tester que tous les moteurs sont dans la liste."""
        from backend.engines import ENGINES, ENGINES_BY_NAME
        
        expected_engines = [
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
        
        assert len(ENGINES) == 14
        assert set(ENGINES) == set(expected_engines)
        assert len(ENGINES_BY_NAME) == 14


# État du module
MODULE_STATUS = "IMPLEMENTED"
