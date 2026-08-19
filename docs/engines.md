# HexLegIA - Les 14 Moteurs

## 🚀 Introduction

HexLegIA est construit autour de **14 moteurs spécialisés** qui fournissent les fonctionnalités métier de la plateforme. Chaque moteur est conçu pour être :

- **Modulaire** : Indépendant des autres moteurs
- **Extensible** : Facile à étendre avec de nouvelles fonctionnalités
- **Testable** : Tests unitaires et d'intégration isolés
- **Intégrable** : Communication claire avec les autres composants

## 📋 Liste des Moteurs

| # | Moteur | Rôle | État | Priorité |
|---|--------|------|------|----------|
| 1 | **VerificationEngine** | Vérification des données et identités | SCAFFOLD | ⭐⭐⭐⭐ |
| 2 | **ContextEngine** | Centralisation du contexte utilisateur et organisationnel | SCAFFOLD | ⭐⭐⭐⭐⭐ |
| 3 | **AccessDecisionEngine** | Contrôle centralisé des accès (RBAC/ABAC) | SCAFFOLD | ⭐⭐⭐⭐⭐ |
| 4 | **AIOrchestrator** | Orchestration des fournisseurs IA | SCAFFOLD | ⭐⭐⭐⭐⭐ |
| 5 | **SimulationEngine** | Simulation de scénarios | SCAFFOLD | ⭐⭐⭐ |
| 6 | **RiskEngine** | Évaluation des risques | SCAFFOLD | ⭐⭐⭐⭐ |
| 7 | **DecisionEngine** | Prise de décision automatisée | SCAFFOLD | ⭐⭐⭐⭐ |
| 8 | **ActionEngine** | Exécution d'actions | SCAFFOLD | ⭐⭐⭐ |
| 9 | **KnowledgeGraphEngine** | Gestion du graphe de connaissances | SCAFFOLD | ⭐⭐ |
| 10 | **WorkflowEngine** | Orchestration des workflows | SCAFFOLD | ⭐⭐⭐ |
| 11 | **CollaborationEngine** | Gestion de la collaboration | SCAFFOLD | ⭐⭐ |
| 12 | **NotificationEngine** | Système de notifications | SCAFFOLD | ⭐⭐ |
| 13 | **DocumentGenerator** | Génération de documents | SCAFFOLD | ⭐⭐ |
| 14 | **ConnectorEngine** | Connecteurs externes | SCAFFOLD | ⭐⭐ |

## 🔍 Détail des Moteurs

### 1. VerificationEngine

**Rôle :** Vérification des données et identités

**Responsabilités :**
- Vérifier l'intégrité des données
- Valider les identités utilisateurs
- Vérifier les signatures et certificats
- Détecter les anomalies
- Fournir des scores de confiance

**Types de vérification :**
- `IDENTITY` : Vérification des identités
- `DATA` : Vérification de l'intégrité des données
- `SIGNATURE` : Vérification des signatures
- `CERTIFICATE` : Vérification des certificats
- `INTEGRITY` : Vérification de l'intégrité
- `AUTHENTICITY` : Vérification de l'authenticité

**Modèles :**
```python
class VerificationRequest(BaseModel):
    verification_type: VerificationType
    target: str
    data: Optional[Dict[str, Any]]
    context: Dict[str, Any]
    requester: Optional[str]
    priority: int

class VerificationResult(BaseModel):
    request: VerificationRequest
    status: VerificationStatus  # PENDING, SUCCESS, FAILED, ERROR
    result: Optional[Dict[str, Any]]
    score: Optional[float]  # Score de confiance (0-1)
    issues: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
    duration_ms: float
```

**Exemple d'utilisation :**
```python
engine = VerificationEngine()
result = await engine.verify(
    verification_type=VerificationType.IDENTITY,
    target="user_123",
    data={"token": "abc123"},
    context={"ip": "192.168.1.1"},
)
```

**État :** SCAFFOLD - Structure de base implémentée, logique métier à développer

---

### 2. ContextEngine

**Rôle :** Centralisation du contexte

**Responsabilités :**
- Gérer le contexte utilisateur
- Maintenir le contexte organisationnel
- Fournir le contexte temporel et réglementaire
- Centraliser l'historique nécessaire aux décisions

**Types de contexte :**
- `USER` : Contexte utilisateur (rôles, permissions, attributs)
- `ORGANIZATION` : Contexte organisationnel (politiques, conformité)
- `REQUEST` : Contexte de la requête (ressource, action, headers)
- `TEMPORAL` : Contexte temporel (date, heure, timezone)
- `REGULATORY` : Contexte réglementaire (juridiction, lois applicables)
- `HISTORICAL` : Contexte historique (historique des actions)

**Modèles :**
```python
class UserContext(BaseModel):
    user_id: str
    username: str
    roles: List[str]
    permissions: List[str]
    is_authenticated: bool
    attributes: Dict[str, Any]

class Context(BaseModel):
    user_context: Optional[UserContext]
    organization_context: Optional[OrganizationContext]
    request_context: Optional[RequestContext]
    temporal_context: Optional[TemporalContext]
    regulatory_context: Optional[RegulatoryContext]
    historical_context: Optional[HistoricalContext]
```

**Exemple d'utilisation :**
```python
engine = ContextEngine()
user_context = await engine.create_user_context(
    user_id="user_123",
    username="john.doe",
    roles=["admin", "user"],
    is_authenticated=True,
)
full_context = await engine.get_full_context(
    user_id="user_123",
    organization_id="org_1",
)
```

**État :** SCAFFOLD - Structure complète implémentée, intégration avec autres moteurs à finaliser

---

### 3. AccessDecisionEngine

**Rôle :** Contrôle centralisé des accès

**⚠️ COMPOSANT CRITIQUE**

**Principe :**
```
Utilisateur / IA
       ↓
Authentification
       ↓
ACCESS DECISION ENGINE
       ↓
Autorisé ?
   ↓          ↓
 OUI         NON
  ↓           ↓
Accès       Refus
```

**Aucun service manipulant une donnée sensible ou exécutant une action protégée ne doit pouvoir contourner ce mécanisme.**

**Éléments du contrat :**
- Identité du demandeur
- Type de demandeur (HUMAN, AI, SERVICE, SYSTEM)
- Ressource demandée
- Action demandée
- Contexte
- Justification
- Niveau de sensibilité (PUBLIC, INTERNAL, CONFIDENTIAL, SECRET)
- Décision (ALLOWED, DENIED, PENDING, CONDITIONAL)
- Raison de la décision
- Trace d'audit

**Politiques supportées :**
- **RBAC** : Role-Based Access Control
- **ABAC** : Attribute-Based Access Control

**Modèles :**
```python
class AccessDecisionRequest(BaseModel):
    requester: str
    requester_type: RequesterType
    resource: str
    action: str
    context: Dict[str, Any]
    justification: Optional[str]
    sensitivity_level: SensitivityLevel

class AccessDecisionResponse(BaseModel):
    request: AccessDecisionRequest
    decision: DecisionType
    allowed: bool
    reason: Optional[str]
    justification: Optional[str]
    conditions: List[str]
    policies_applied: List[str]
    audit_trace: Dict[str, Any]
    confidence_score: float
```

**Exemple d'utilisation :**
```python
engine = AccessDecisionEngine()
decision = await engine.check_access(
    requester="user_123",
    requester_type=RequesterType.HUMAN,
    resource="/admin/users",
    action="GET",
    context={"ip": "192.168.1.1"},
    sensitivity_level=SensitivityLevel.CONFIDENTIAL,
)

if decision.allowed:
    # Accorder l'accès
    pass
else:
    # Refuser l'accès
    raise HTTPException(status_code=403, detail=decision.reason)
```

**État :** SCAFFOLD - Structure complète avec politiques par défaut, intégration avec ContextEngine à finaliser

---

### 4. AIOrchestrator

**Rôle :** Orchestration des fournisseurs IA

**Architecture :**
```
AIOrchestrator
      ↓
AI Provider Interface
      ↓
┌──────────┬──────────┬──────────┐
│ Mistral  │ OpenAI   │  Autre   │
└──────────┴──────────┴──────────┘
```

**Les moteurs ne doivent pas appeler directement un fournisseur IA. Le fournisseur doit être interchangeable.**

**Fournisseurs implémentés :**
- **MistralAIProvider** : Intégration avec l'API Mistral
- **OpenAIProvider** : Intégration avec l'API OpenAI

**Fonctionnalités :**
- Abstraction des fournisseurs
- Gestion des erreurs et timeouts
- Fallback entre fournisseurs
- Traçabilité des appels
- Métriques d'utilisation

**Types de modèles :**
- `TEXT` : Génération de texte
- `CHAT` : Chat conversationnel
- `EMBEDDING` : Embeddings vectoriels
- `IMAGE` : Génération d'images
- `AUDIO` : Traitement audio
- `VIDEO` : Traitement vidéo
- `MULTIMODAL` : Modèles multimodaux

**Modèles :**
```python
class AIRequest(BaseModel):
    provider_type: Optional[AIProviderType]
    model: str
    model_type: AIModelType
    prompt: Optional[str]
    messages: Optional[List[Dict[str, Any]]]
    input: Optional[Any]
    parameters: Dict[str, Any]
    context: Dict[str, Any]

class AIResponse(BaseModel):
    request: AIRequest
    provider_type: AIProviderType
    model: str
    model_type: AIModelType
    output: Any
    usage: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str]
    duration_ms: float
```

**Exemple d'utilisation :**
```python
orchestrator = AIOrchestrator()

# Requête de chat
response = await orchestrator.chat(
    model="mistral-tiny",
    messages=[
        {"role": "user", "content": "Bonjour !"},
    ],
    temperature=0.7,
)

# Requête d'embedding
embedding_response = await orchestrator.embed(
    model="mistral-embed",
    input="Texte à embedder",
)
```

**État :** SCAFFOLD - Structure complète avec fournisseurs Mistral et OpenAI, tests d'intégration à ajouter

---

### 5. SimulationEngine

**Rôle :** Simulation de scénarios

**Responsabilités :**
- Simuler des scénarios complexes
- Tester des hypothèses
- Évaluer des impacts
- Générer des prédictions

**Types de simulation :**
- `SCENARIO` : Simulation de scénarios personnalisés
- `MONTE_CARLO` : Simulation Monte Carlo
- `TIME_SERIES` : Analyse de séries temporelles
- `AGENT_BASED` : Simulation basée sur des agents
- `SYSTEM_DYNAMICS` : Dynamique des systèmes

**Modèles :**
```python
class SimulationRequest(BaseModel):
    simulation_type: SimulationType
    name: str
    description: Optional[str]
    parameters: Dict[str, Any]
    initial_conditions: Dict[str, Any]
    constraints: List[Dict[str, Any]]
    timeout_seconds: float

class SimulationResult(BaseModel):
    request: SimulationRequest
    status: SimulationStatus  # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
    results: Dict[str, Any]
    metrics: Dict[str, Any]
    visualizations: List[Dict[str, Any]]
    warnings: List[str]
    errors: List[str]
    duration_seconds: float
```

**Exemple d'utilisation :**
```python
engine = SimulationEngine()
result = await engine.run_simulation(
    simulation_type=SimulationType.SCENARIO,
    name="simulation_test",
    parameters={"iterations": 1000},
    initial_conditions={"population": 1000},
    timeout_seconds=60.0,
)
```

**État :** SCAFFOLD - Structure de base implémentée

---

### 6. RiskEngine

**Rôle :** Évaluation des risques

**Responsabilités :**
- Évaluer les risques
- Analyser les vulnérabilités
- Calculer les scores de risque
- Générer des alertes

**Catégories de risque :**
- `SECURITY` : Risques de sécurité
- `COMPLIANCE` : Risques de conformité
- `OPERATIONAL` : Risques opérationnels
- `FINANCIAL` : Risques financiers
- `REPUTATIONAL` : Risques de réputation
- `LEGAL` : Risques juridiques

**Niveaux de risque :**
- `LOW` : Risque faible
- `MEDIUM` : Risque moyen
- `HIGH` : Risque élevé
- `CRITICAL` : Risque critique

**Modèles :**
```python
class RiskAssessmentRequest(BaseModel):
    name: str
    target: str
    risk_categories: List[RiskCategory]
    parameters: Dict[str, Any]
    context: Dict[str, Any]

class RiskAssessmentResult(BaseModel):
    request: RiskAssessmentRequest
    overall_risk_level: RiskLevel
    category_risk_levels: Dict[RiskCategory, RiskLevel]
    risk_scores: Dict[str, float]
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    alerts: List[Dict[str, Any]]
    duration_ms: float
```

**Exemple d'utilisation :**
```python
engine = RiskEngine()
result = await engine.assess_risk(
    name="risk_assessment_1",
    target="user_data_export",
    risk_categories=[RiskCategory.SECURITY, RiskCategory.COMPLIANCE],
    context={"user_id": "user_123"},
)

if result.overall_risk_level == RiskLevel.HIGH:
    # Bloquer l'opération
    pass
```

**État :** SCAFFOLD - Structure complète avec assessors par catégorie

---

### 7. DecisionEngine

**Rôle :** Prise de décision automatisée

**Responsabilités :**
- Prendre des décisions basées sur des règles
- Intégrer avec d'autres moteurs (Risk, Context, etc.)
- Fournir des explications pour les décisions
- Gérer les décisions complexes

**État :** SCAFFOLD - Structure de base implémentée

---

### 8. ActionEngine

**Rôle :** Exécution d'actions

**Responsabilités :**
- Exécuter des actions automatisées
- Gérer les workflows d'actions
- Assurer la traçabilité des actions
- Gérer les erreurs et rollbacks

**État :** SCAFFOLD - Structure de base implémentée

---

### 9. KnowledgeGraphEngine

**Rôle :** Gestion du graphe de connaissances

**Responsabilités :**
- Construire et maintenir un graphe de connaissances
- Effectuer des requêtes sur le graphe
- Intégrer avec la recherche vectorielle (Qdrant)
- Fournir des insights basés sur le graphe

**État :** SCAFFOLD - Structure de base implémentée

---

### 10. WorkflowEngine

**Rôle :** Orchestration des workflows

**Responsabilités :**
- Définir et exécuter des workflows
- Gérer les dépendances entre étapes
- Assurer la reprise sur erreur
- Fournir un historique des exécutions

**État :** SCAFFOLD - Structure de base implémentée

---

### 11. CollaborationEngine

**Rôle :** Gestion de la collaboration

**Responsabilités :**
- Gérer les espaces de travail partagés
- Assurer la coordination entre utilisateurs
- Gérer les permissions de collaboration
- Fournir des outils de communication

**État :** SCAFFOLD - Structure de base implémentée

---

### 12. NotificationEngine

**Rôle :** Système de notifications

**Responsabilités :**
- Envoyer des notifications aux utilisateurs
- Gérer les préférences de notification
- Intégrer avec différents canaux (email, web, mobile)
- Assurer la livraison des notifications

**État :** SCAFFOLD - Structure de base implémentée

---

### 13. DocumentGenerator

**Rôle :** Génération de documents

**Responsabilités :**
- Générer des documents structurés
- Supporter différents formats (PDF, Word, etc.)
- Intégrer avec les templates
- Assurer la qualité des documents générés

**État :** SCAFFOLD - Structure de base implémentée

---

### 14. ConnectorEngine

**Rôle :** Connecteurs externes

**Responsabilités :**
- Intégrer avec des systèmes externes
- Gérer les connexions et authentifications
- Assurer la compatibilité avec différents protocoles
- Fournir une abstraction pour les intégrations

**État :** SCAFFOLD - Structure de base implémentée

---

## 🔗 Intégration entre Moteurs

Les moteurs sont conçus pour travailler ensemble. Voici quelques exemples d'intégration :

### Exemple 1 : Décision d'accès avec contexte

```python
# Dans un contrôleur FastAPI
from backend.engines import get_engine

async def protected_endpoint(request: Request):
    # Obtenir les moteurs
    access_engine = get_engine("AccessDecisionEngine")
    context_engine = get_engine("ContextEngine")
    
    # Obtenir le contexte
    full_context = await context_engine.get_context_for_decision(
        requester_id=request.user.id,
        resource="/protected/data",
        action="GET",
    )
    
    # Vérifier l'accès
    decision = await access_engine.check_access(
        requester=request.user.id,
        resource="/protected/data",
        action="GET",
        context=full_context.to_dict(),
    )
    
    if not decision.allowed:
        raise HTTPException(status_code=403, detail=decision.reason)
    
    # Accorder l'accès
    return {"data": "protected_data"}
```

### Exemple 2 : Évaluation de risque avec IA

```python
# Dans un service d'évaluation
async def evaluate_risk_with_ai(target: str, context: dict):
    # Obtenir les moteurs
    risk_engine = get_engine("RiskEngine")
    ai_orchestrator = get_engine("AIOrchestrator")
    
    # Évaluer le risque
    risk_result = await risk_engine.assess_risk(
        name=f"risk_assessment_{target}",
        target=target,
        risk_categories=[RiskCategory.SECURITY],
        context=context,
    )
    
    # Si le risque est élevé, demander une analyse IA
    if risk_result.overall_risk_level == RiskLevel.HIGH:
        ai_response = await ai_orchestrator.chat(
            model="mistral-large",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en sécurité. Analyse le risque suivant et propose des recommandations."
                },
                {
                    "role": "user",
                    "content": f"Risque détecté: {risk_result.findings}"
                },
            ],
        )
        
        risk_result.recommendations.append(ai_response.output)
    
    return risk_result
```

### Exemple 3 : Simulation avec contexte utilisateur

```python
# Dans un service de simulation
async def run_user_simulation(user_id: str, scenario: dict):
    # Obtenir les moteurs
    simulation_engine = get_engine("SimulationEngine")
    context_engine = get_engine("ContextEngine")
    
    # Obtenir le contexte utilisateur
    user_context = await context_engine.get_user_context(user_id)
    
    # Exécuter la simulation avec le contexte
    result = await simulation_engine.run_simulation(
        simulation_type=SimulationType.SCENARIO,
        name=f"simulation_{user_id}",
        parameters=scenario.get("parameters", {}),
        initial_conditions={
            **scenario.get("initial_conditions", {}),
            "user_attributes": user_context.attributes,
        },
    )
    
    return result
```

## 📊 État d'Implémentation

| Moteur | Structure | Modèles | Logique Métier | Tests | Documentation |
|--------|----------|--------|----------------|-------|--------------|
| VerificationEngine | ✅ | ✅ | ❌ | ✅ | ✅ |
| ContextEngine | ✅ | ✅ | ❌ | ✅ | ✅ |
| AccessDecisionEngine | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| AIOrchestrator | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| SimulationEngine | ✅ | ✅ | ❌ | ✅ | ✅ |
| RiskEngine | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| DecisionEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| ActionEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| KnowledgeGraphEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| WorkflowEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| CollaborationEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| NotificationEngine | ✅ | ❌ | ❌ | ✅ | ✅ |
| DocumentGenerator | ✅ | ❌ | ❌ | ✅ | ✅ |
| ConnectorEngine | ✅ | ❌ | ❌ | ✅ | ✅ |

**Légende :**
- ✅ : Implémenté
- ⚠️ : Partiellement implémenté
- ❌ : Non implémenté

## 🎯 Prochaines Étapes

1. **Finaliser l'intégration** entre les moteurs
2. **Implémenter la logique métier** pour chaque moteur
3. **Ajouter des tests complets** pour chaque moteur
4. **Documenter les cas d'utilisation** pour chaque moteur
5. **Optimiser les performances** des moteurs critiques
6. **Ajouter le monitoring** pour suivre l'utilisation des moteurs

## 📚 Bonnes Pratiques

1. **Ne pas contourner le AccessDecisionEngine** pour les opérations sensibles
2. **Utiliser le ContextEngine** pour centraliser les informations de contexte
3. **Passer par l'AIOrchestrator** pour toutes les requêtes IA
4. **Gérer les erreurs** de manière cohérente dans tous les moteurs
5. **Logger les opérations** importantes pour l'audit
6. **Documenter les contrats** de chaque moteur
7. **Écrire des tests** pour chaque fonctionnalité
8. **Respecter les interfaces** définies pour chaque moteur
