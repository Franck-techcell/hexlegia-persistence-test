# HexLegIA - Architecture

## 📐 Architecture Générale

HexLegIA suit une architecture modulaire et séparée en plusieurs couches distinctes pour assurer la maintenabilité, l'extensibilité et la sécurité.

### Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   React     │  │  TypeScript │  │   Material  │  │    Axios    │    │
│  │   (18.x)    │  │    (5.x)    │  │     UI      │  │  (HTTP)     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        Application Layer                           │  │
│  │  app/          - Composants principaux                            │  │
│  │  components/   - Composants réutilisables                          │  │
│  │  services/     - Services API                                      │  │
│  │  types/        - Types TypeScript                                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                      ↓
                                      HTTP/HTTPS
                                      ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        API Layer (FastAPI)                         │  │
│  │  api/          - Routes et contrôleurs                            │  │
│  │  │   routes/   - Endpoints REST                                   │  │
│  │  │   middleware/- Middlewares (sécurité, audit, etc.)              │  │
│  │  └─────────────────────────────────────────────────────────────┘  │
│  │                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │                        Core Layer                               │  │  │
│  │  │  core/        - Configuration, logging, exceptions              │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │                        Security Layer                            │  │  │
│  │  │  security/     - Authentification, autorisation, audit          │  │  │
│  │  │  │   access_control.py - AccessDecisionEngine                  │  │  │
│  │  │  │   authentication.py - Gestion des utilisateurs               │  │  │
│  │  │  │   authorization.py - Gestion des permissions                 │  │  │
│  │  │  │   audit.py         - Traçage des opérations                 │  │  │
│  │  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  │                                                                 │  │
│  │  │  ┌─────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                        Engines Layer                           │  │  │  │
│  │  │  │  engines/      - 14 moteurs spécialisés                       │  │  │  │
│  │  │  │  │   verification/       - Vérification des données          │  │  │  │
│  │  │  │  │   context/            - Gestion du contexte               │  │  │  │
│  │  │  │  │   access_decision/    - Décision d'accès centralisée     │  │  │  │
│  │  │  │  │   ai_orchestrator/    - Orchestration IA                  │  │  │  │
│  │  │  │  │   simulation/         - Simulation de scénarios            │  │  │  │
│  │  │  │  │   risk/               - Évaluation des risques             │  │  │  │
│  │  │  │  │   decision/           - Prise de décision                  │  │  │  │
│  │  │  │  │   action/             - Exécution d'actions               │  │  │  │
│  │  │  │  │   knowledge_graph/    - Graphe de connaissances            │  │  │  │
│  │  │  │  │   workflow/           - Orchestration de workflows         │  │  │  │
│  │  │  │  │   collaboration/      - Gestion de la collaboration        │  │  │  │
│  │  │  │  │   notification/       - Système de notifications           │  │  │  │
│  │  │  │  │   document_generator/ - Génération de documents           │  │  │  │
│  │  │  │  └── connector/          - Connecteurs externes              │  │  │  │
│  │  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  │                                                                 │  │
│  │  │  ┌─────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                        Services Layer                         │  │  │  │
│  │  │  │  services/     - Services métier                             │  │  │  │
│  │  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  │                                                                 │  │
│  │  │  ┌─────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                        Persistence Layer                      │  │  │  │
│  │  │  │  models/       - Modèles SQLAlchemy                         │  │  │  │
│  │  │  │  schemas/      - Schémas Pydantic                            │  │  │  │
│  │  │  │  repositories/ - Repository pattern                           │  │  │  │
│  │  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │
│  └─────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────┘
                                      ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                              DATABASE                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                      │
│  │     PostgreSQL       │  │        Qdrant         │                      │
│  │  (Données structurées)│  │  (Recherche vectorielle)│                      │
│  └─────────────────────┘  └─────────────────────┘                      │
│                                                                         │
│  database/                                                               │
│  ├── migrations/     - Migrations Alembic                             │
│  └── seeds/          - Données initiales                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🏗️ Couches de l'Architecture

### 1. Frontend Layer

**Technologies :** React 18, TypeScript, Material UI, Axios

**Responsabilités :**
- Interface utilisateur
- Gestion de l'état local
- Appels API vers le backend
- Affichage des données

**Structure :**
```
frontend/
├── public/          # Fichiers statiques
├── src/            # Code source
│   ├── index.tsx   # Point d'entrée
│   ├── App.tsx     # Composant principal
│   ├── app/        # Composants applicatifs
│   ├── components/ # Composants réutilisables
│   ├── services/   # Services API
│   └── types/      # Types TypeScript
└── package.json    # Dépendances
```

### 2. API Layer (FastAPI)

**Technologies :** FastAPI, Pydantic, Uvicorn

**Responsabilités :**
- Définition des endpoints REST
- Validation des requêtes/réponses
- Gestion des middlewares
- Routage des requêtes

**Structure :**
```
backend/api/
├── main.py         # Application FastAPI
├── routes/         # Définition des routes
│   └── health.py   # Endpoint de santé
└── middleware/     # Middlewares personnalisés
    ├── request_id.py
    ├── audit.py
    ├── security.py
    └── error_handler.py
```

### 3. Core Layer

**Responsabilités :**
- Configuration centrale
- Gestion du logging
- Définition des exceptions
- Utilitaires partagés

**Structure :**
```
backend/core/
├── __init__.py
├── config.py      # Configuration Pydantic
├── logging.py     # Configuration du logging
└── exceptions.py  # Hiérarchie d'exceptions
```

### 4. Security Layer

**Responsabilités :**
- Authentification des utilisateurs
- Autorisation (RBAC/ABAC)
- Contrôle d'accès centralisé
- Audit des opérations
- Gestion des secrets

**Structure :**
```
backend/security/
├── __init__.py
├── models.py      # Modèles de sécurité
├── access_control.py  # AccessDecisionEngine
├── authentication.py  # Service d'authentification
├── authorization.py   # Service d'autorisation
├── audit.py          # Service d'audit
└── policies.py       # Politiques RBAC/ABAC
```

### 5. Engines Layer

**Responsabilités :**
- Implémentation des 14 moteurs spécialisés
- Logique métier centralisée
- Traitement des données
- Intégration avec les services externes

**Structure :**
```
backend/engines/
├── __init__.py      # Initialisation des moteurs
├── verification/    # Moteur de vérification
├── context/         # Moteur de contexte
├── access_decision/ # Moteur de décision d'accès
├── ai_orchestrator/ # Orchestrateur IA
├── simulation/      # Moteur de simulation
├── risk/            # Moteur de risque
├── decision/        # Moteur de décision
├── action/          # Moteur d'action
├── knowledge_graph/ # Moteur de graphe de connaissances
├── workflow/        # Moteur de workflow
├── collaboration/   # Moteur de collaboration
├── notification/    # Moteur de notification
├── document_generator/ # Générateur de documents
└── connector/       # Connecteurs externes
```

### 6. Persistence Layer

**Technologies :** SQLAlchemy, AsyncPG, Alembic

**Responsabilités :**
- Définition des modèles de données
- Implémentation du Repository Pattern
- Gestion des connexions
- Exécution des migrations

**Structure :**
```
backend/
├── models/         # Modèles SQLAlchemy
├── schemas/        # Schémas Pydantic
├── repositories/   # Implémentations Repository
└── database/       # Configuration DB
    ├── migrations/ # Migrations Alembic
    └── seeds/      # Données initiales
```

## 🔄 Flux de Requêtes

### Flux Standard

```
1. Requête HTTP → Frontend (React)
2. Appel API → Backend (FastAPI)
3. Middleware → Vérification sécurité, audit, etc.
4. Routeur → Trouver le contrôleur approprié
5. Service → Traitement métier
6. Engine → Logique spécialisée
7. Repository → Accès aux données
8. Réponse → Retour au frontend
```

### Flux avec Contrôle d'Accès

```
1. Requête HTTP → Frontend
2. Appel API → Backend
3. Security Middleware → Vérification JWT
4. AccessDecisionEngine → Décision d'accès
   ├─ Vérification des politiques RBAC/ABAC
   ├─ Vérification du contexte
   └─ Génération de la trace d'audit
5. Si autorisé → Continuer vers le contrôleur
6. Si refusé → Retour 403 Forbidden
```

### Flux avec Orchestration IA

```
1. Requête → Frontend
2. Appel API → Backend
3. Contrôleur → Appel AIOrchestrator
4. AIOrchestrator → Sélection du fournisseur
5. Provider (Mistral/OpenAI) → Exécution du modèle
6. Réponse → Retour à l'orchestrateur
7. Traitement → Intégration des résultats
8. Réponse finale → Retour au frontend
```

## 🔒 Architecture de Sécurité

### Principe de Base

**Aucun service manipulant une donnée sensible ou exécutant une action protégée ne doit pouvoir contourner le AccessDecisionEngine.**

```
┌─────────────────────────────────────────────────────────────┐
│                    ACCESS DECISION ENGINE                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Vérification :                                          ││
│  │  - Identité du demandeur                                ││
│  │  - Type de demandeur (user, ai, service, system)         ││
│  │  - Ressource demandée                                    ││
│  │  - Action demandée                                       ││
│  │  - Contexte                                              ││
│  │  - Justification                                         ││
│  │  - Niveau de sensibilité                                ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Décision :                                              ││
│  │  - Autorisé ? (OUI/NON)                                  ││
│  │  - Raison de la décision                                 ││
│  │  - Trace d'audit                                         ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┐
                    │  OUI    │
                    ↓         ↓
              ┌─────────┐ ┌─────────┐
              │ Accès   │ │ Refus   │
              │ autorisé│ │ (403)   │
              └─────────┘ └─────────┘
```

### Politiques d'Accès

HexLegIA supporte deux types de politiques :

1. **RBAC (Role-Based Access Control)**
   - Basé sur les rôles des utilisateurs
   - Simple et efficace pour les structures hiérarchiques
   - Exemple : "Les administrateurs peuvent tout faire"

2. **ABAC (Attribute-Based Access Control)**
   - Basé sur les attributs (utilisateur, ressource, contexte)
   - Plus flexible et granulaire
   - Exemple : "Les utilisateurs du département X peuvent accéder aux données Y entre 9h et 17h"

### Mécanisme d'Audit

Chaque opération importante est tracée avec :
- **Qui** : Identité du demandeur
- **Quoi** : Ressource et action
- **Quand** : Timestamp
- **Pourquoi** : Justification
- **Résultat** : Succès ou échec

## 🛠️ Patterns Utilisés

### 1. Repository Pattern

Sépare la logique métier de l'accès aux données.

```python
# Repository
class UserRepository:
    async def get_by_id(self, user_id: str) -> User:
        # Logique d'accès à la base de données
        pass

# Service
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def get_user(self, user_id: str) -> User:
        # Logique métier
        return await self.repository.get_by_id(user_id)
```

### 2. Dependency Injection

Utilisé avec FastAPI pour une meilleure testabilité.

```python
from fastapi import Depends

async def get_user_service() -> UserService:
    return UserService(UserRepository())

@app.get("/users/{user_id}")
async def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)
```

### 3. Strategy Pattern

Utilisé pour les fournisseurs IA interchangeables.

```python
class BaseAIProvider(ABC):
    @abstractmethod
    async def execute(self, request: AIRequest) -> AIResponse:
        pass

class MistralAIProvider(BaseAIProvider):
    async def execute(self, request: AIRequest) -> AIResponse:
        # Implémentation spécifique Mistral
        pass

class AIOrchestrator:
    def __init__(self):
        self.providers = {
            AIProviderType.MISTRAL: MistralAIProvider(),
            AIProviderType.OPENAI: OpenAIProvider(),
        }
```

### 4. Middleware Pattern

Pour le traitement transversal des requêtes.

```python
from fastapi import Request

async def audit_middleware(request: Request, call_next):
    # Pré-traitement
    start_time = time.time()
    
    response = await call_next(request)
    
    # Post-traitement
    duration = time.time() - start_time
    log_audit(request, response, duration)
    
    return response
```

## 📊 Intégration des Technologies

### PostgreSQL

- **Utilisation** : Données structurées, relations
- **Client** : AsyncPG (asynchrone)
- **ORM** : SQLAlchemy 2.0
- **Migrations** : Alembic

### Qdrant

- **Utilisation** : Recherche vectorielle, embeddings
- **Client** : qdrant-client
- **Intégration** : Via AIOrchestrator pour les embeddings

### Docker

- **Conteneurs** : Frontend, Backend, PostgreSQL, Qdrant
- **Orchestration** : Docker Compose
- **Réseau** : Réseau dédié pour la communication interne

## 🎯 Bonnes Pratiques

1. **Séparation des responsabilités** : Chaque couche a un rôle clair
2. **Injection de dépendances** : Pour une meilleure testabilité
3. **Validation des données** : Utilisation de Pydantic pour la validation
4. **Logging structuré** : Utilisation de structlog pour des logs exploitables
5. **Gestion des erreurs** : Hiérarchie d'exceptions personnalisées
6. **Documentation** : Docstrings et documentation technique
7. **Tests** : Tests unitaires et d'intégration

## 🔮 Évolution Future

- **Microservices** : Décomposition en microservices si nécessaire
- **Event Sourcing** : Pour l'historique des changements
- **CQRS** : Séparation lecture/écriture pour la performance
- **GraphQL** : Alternative à REST pour les requêtes complexes
- **Serverless** : Déploiement sur des fonctions serverless
