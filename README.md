# HexLegIA - Socle Technique V1

## 🎯 Objectif du Projet

HexLegIA est une plateforme technique conçue pour héberger 14 moteurs spécialisés dans la gestion intelligente des accès, des décisions, des risques et de l'orchestration IA. Ce socle technique V1 établit l'architecture de base nécessaire pour le développement progressif de ces moteurs.

## 🏗️ Architecture

L'architecture suit une séparation claire entre :
- **Frontend** : Interface utilisateur en React/TypeScript
- **Backend** : API FastAPI avec les moteurs métier
- **Moteurs** : 14 modules spécialisés (voir [Engines](#-les-14-moteurs))
- **Sécurité** : Couche dédiée pour l'authentification et l'autorisation
- **Persistance** : PostgreSQL pour les données structurées, Qdrant pour la recherche vectorielle
- **Infrastructure** : Docker et Docker Compose

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | React 18 + TypeScript |
| Backend | Python 3.11 + FastAPI |
| Base de données | PostgreSQL 15 |
| Recherche vectorielle | Qdrant |
| Conteneurisation | Docker + Docker Compose |
| Tests Backend | Pytest |
| Tests Frontend | Vitest + React Testing Library |

## 📁 Structure des Dossiers

```
HEXLEGIA/
├── frontend/                    # Application React
│   ├── app/                    # Composants principaux
│   ├── components/             # Composants réutilisables
│   ├── services/               # Services API
│   └── types/                  # Types TypeScript
│
├── backend/                    # API FastAPI
│   ├── api/                    # Routes et contrôleurs
│   ├── core/                   # Configuration et utilitaires
│   ├── engines/                # 14 moteurs métier
│   │   ├── verification/       # Moteur de vérification
│   │   ├── context/            # Moteur de contexte
│   │   ├── access_decision/    # Moteur de décision d'accès
│   │   ├── ai_orchestrator/    # Orchestrateur IA
│   │   ├── simulation/         # Moteur de simulation
│   │   ├── risk/               # Moteur de risque
│   │   ├── decision/           # Moteur de décision
│   │   ├── action/             # Moteur d'action
│   │   ├── knowledge_graph/    # Moteur de graphe de connaissances
│   │   ├── workflow/           # Moteur de workflow
│   │   ├── collaboration/      # Moteur de collaboration
│   │   ├── notification/       # Moteur de notification
│   │   ├── document_generator/ # Générateur de documents
│   │   └── connector/          # Connecteurs externes
│   │
│   ├── models/                 # Modèles de données
│   ├── schemas/                # Schémas Pydantic
│   ├── repositories/           # Couche de persistance
│   ├── security/               # Sécurité et autorisation
│   └── services/               # Services métier
│
├── database/                   # Base de données
│   ├── migrations/             # Migrations Alembic
│   └── seeds/                  # Données initiales
│
├── tests/                      # Tests
│   ├── unit/                   # Tests unitaires
│   ├── integration/            # Tests d'intégration
│   └── security/               # Tests de sécurité
│
├── docs/                       # Documentation
│   ├── architecture.md         # Architecture détaillée
│   ├── engines.md              # Documentation des moteurs
│   ├── security.md             # Documentation sécurité
│   └── development.md          # Guide de développement
│
├── docker/                     # Configuration Docker
├── .env.example                # Variables d'environnement
├── docker-compose.yml          # Orchestration Docker
└── README.md                   # Documentation principale
```

## 🚀 Les 14 Moteurs

| # | Moteur | Rôle | État |
|---|--------|------|------|
| 1 | VerificationEngine | Vérification des données et identités | SCAFFOLD |
| 2 | ContextEngine | Centralisation du contexte utilisateur et organisationnel | SCAFFOLD |
| 3 | AccessDecisionEngine | Contrôle centralisé des accès (RBAC/ABAC) | SCAFFOLD |
| 4 | AIOrchestrator | Orchestration des fournisseurs IA | SCAFFOLD |
| 5 | SimulationEngine | Simulation de scénarios | SCAFFOLD |
| 6 | RiskEngine | Évaluation des risques | SCAFFOLD |
| 7 | DecisionEngine | Prise de décision automatisée | SCAFFOLD |
| 8 | ActionEngine | Exécution d'actions | SCAFFOLD |
| 9 | KnowledgeGraphEngine | Gestion du graphe de connaissances | SCAFFOLD |
| 10 | WorkflowEngine | Orchestration des workflows | SCAFFOLD |
| 11 | CollaborationEngine | Gestion de la collaboration | SCAFFOLD |
| 12 | NotificationEngine | Système de notifications | SCAFFOLD |
| 13 | DocumentGenerator | Génération de documents | SCAFFOLD |
| 14 | ConnectorEngine | Connecteurs externes | SCAFFOLD |

## 📋 État Réel de l'Implémentation

### ✅ IMPLEMENTED
- Structure complète du projet
- Configuration Docker et Docker Compose
- API FastAPI minimale avec endpoint `/health`
- Frontend React minimal
- Configuration PostgreSQL et Qdrant
- Couche de sécurité de base
- Mécanisme d'audit transversal
- Tests minimaux pour tous les composants

### 🏗️ SCAFFOLD
- Les 14 moteurs (interfaces, structures, contrats)
- Modèles de données de base
- Schémas Pydantic
- Repository layer
- AI Provider Interface
- RBAC/ABAC framework (préparation)

### ❌ NOT_IMPLEMENTED
- Logique métier complète des 14 moteurs
- Intégration fonctionnelle avec Qdrant
- Système RAG complet
- Authentification JWT complète
- Politiques RBAC/ABAC opérationnelles
- Interface utilisateur métier

## 🚀 Lancement Local

### Prérequis
- Docker
- Docker Compose
- Git

### Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Franck-techcell/hexlegia-persistence-test.git
   cd hexlegia-persistence-test
   ```

2. Copier le fichier d'environnement :
   ```bash
   cp .env.example .env
   ```

3. Lancer les services :
   ```bash
   docker-compose up -d
   ```

4. Vérifier le backend :
   ```bash
   curl http://localhost:8000/health
   ```

5. Accéder au frontend :
   Ouvrir [http://localhost:3000](http://localhost:3000) dans votre navigateur.

### Arrêt

```bash
docker-compose down
```

## 🔧 Variables d'Environnement

Voir `.env.example` pour la liste complète des variables.

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `POSTGRES_USER` | Utilisateur PostgreSQL | `hexlegia` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `hexlegia_password` |
| `POSTGRES_DB` | Base de données PostgreSQL | `hexlegia_db` |
| `QDRANT_HOST` | Hôte Qdrant | `qdrant` |
| `QDRANT_PORT` | Port Qdrant | `6333` |
| `BACKEND_PORT` | Port du backend | `8000` |
| `FRONTEND_PORT` | Port du frontend | `3000` |
| `SECRET_KEY` | Clé secrète pour JWT | `change-me-in-production` |

## 🧪 Tests

### Backend

```bash
# Dans le conteneur backend
docker-compose exec backend pytest

# Ou localement (après installation des dépendances)
python -m pytest tests/
```

### Frontend

```bash
# Dans le conteneur frontend
npm test
```

### Couverture

```bash
# Backend
pytest --cov=backend tests/

# Frontend
npm run test:coverage
```

## 📝 Documentation

- [Architecture détaillée](docs/architecture.md)
- [Documentation des moteurs](docs/engines.md)
- [Sécurité](docs/security.md)
- [Guide de développement](docs/development.md)

## 🤝 Contribution

1. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
2. Commiter vos changements : `git commit -m 'Ajout de ma fonctionnalite'`
3. Pousser vers la branche : `git push origin feature/ma-fonctionnalite`
4. Ouvrir une Pull Request

## 📄 Licence

Propriétaire - Franck-techcell

## 📞 Contact

Pour toute question, contacter l'équipe technique HexLegIA.
