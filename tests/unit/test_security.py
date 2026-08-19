"""
Security Tests
=============

Tests pour la couche de sécurité.
"""

import pytest
from backend.security.access_control import AccessDecisionEngine
from backend.security.models import (
    AccessRequest,
    AccessDecision,
    DecisionType,
    UserType,
    SensitivityLevel,
)


class TestAccessDecisionEngine:
    """Tests pour le AccessDecisionEngine."""
    
    def test_access_decision_engine_initialization(self):
        """Tester l'initialisation du AccessDecisionEngine."""
        engine = AccessDecisionEngine()
        assert engine.name == "AccessDecisionEngine"
        assert len(engine.policies) > 0
    
    def test_default_deny(self):
        """Tester que l'accès est refusé par défaut."""
        import asyncio
        
        engine = AccessDecisionEngine()
        
        async def test():
            decision = await engine.check_access(
                requester="test_user",
                resource="/test",
                action="GET",
            )
            
            assert decision.allowed == False
            assert decision.decision == DecisionType.DENIED
            assert "default" in decision.reason.lower() or "no policy" in decision.reason.lower()
        
        asyncio.run(test())
    
    def test_access_with_justification(self):
        """Tester l'accès avec justification."""
        import asyncio
        
        engine = AccessDecisionEngine()
        
        async def test():
            # Cela devrait lever une exception car la justification est requise
            with pytest.raises(Exception):
                await engine.check_access_with_justification(
                    requester="test_user",
                    resource="/test",
                    action="GET",
                    justification="",
                )
        
        asyncio.run(test())


# État du module
MODULE_STATUS = "IMPLEMENTED"
