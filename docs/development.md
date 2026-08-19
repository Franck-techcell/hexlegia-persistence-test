# HexLegIA - Guide de Développement

## 🚀 Introduction

Ce guide vous accompagne dans le développement sur la plateforme HexLegIA. Il couvre l'installation, la configuration, les bonnes pratiques et les procédures de contribution.

## 📥 Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- **Git** (version 2.30 ou supérieure)
- **Docker** (version 20.10 ou supérieure)
- **Docker Compose** (version 1.29 ou supérieure)
- **Python** 3.11 (optionnel, pour le développement local)
- **Node.js** 18.x (optionnel, pour le développement local du frontend)

### Cloner le Dépôt

```bash
git clone https://github.com/Franck-techcell/hexlegia-persistence-test.git
cd hexlegia-persistence-test
```

### Configuration de l'Environnement

1. **Copier le fichier d'environnement** :
   ```bash
   cp .env.example .env
   ```

2. **Modifier le fichier `.env`** selon vos besoins :
   ```bash
   # Exemple de configuration locale
   POSTGRES_USER=hexlegia
   POSTGRES_PASSWORD=hexlegia_password
   POSTGRES_DB=hexlegia_db
   SECRET_KEY=my-local-secret-key
   BACKEND_DEBUG=true
   ```

3. **⚠️ NE JAMAIS COMMITTER LE FICHIER `.env`** avec de vrais secrets !

## 🚀 Lancement des Services

### Avec Docker Compose (Recommandé)

```bash
# Lancer tous les services
docker-compose up -d

# Vérifier que les services sont en cours d'exécution
docker-compose ps

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Services Disponibles

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| Backend | http://localhost:8000 | 8000 | API FastAPI |
| Frontend | http://localhost:3000 | 3000 | Application React |
| PostgreSQL | postgres://localhost:5432 | 5432 | Base de données |
| Qdrant | http://localhost:6333 | 6333 | Recherche vectorielle |
| pgAdmin | http://localhost:5050 | 5050 | Interface PostgreSQL (optionnel) |

### Vérification du Déploiement

1. **Vérifier le backend** :
   ```bash
   curl http://localhost:8000/health
   ```
   
   Devrait retourner :
   ```json
   {
     "status": "ok",
     "app": "HexLegIA",
     "version": "1.0.0",
     "timestamp": "...",
     "debug": true
   }
   ```

2. **Vérifier le frontend** :
   Ouvrir [http://localhost:3000](http://localhost:3000) dans votre navigateur.

3. **Vérifier PostgreSQL** :
   ```bash
   docker-compose exec postgres psql -U hexlegia -d hexlegia_db -c "SELECT 1;"
   ```

4. **Vérifier Qdrant** :
   ```bash
   curl http://localhost:6333/readyz
   ```

## 🛠️ Développement Local

### Backend (Python/FastAPI)

#### Installation des Dépendances

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Linux/Mac
source venv/bin/activate

# Sur Windows
venv\Scripts\activate

# Installer les dépendances
pip install -r backend/requirements.txt
```

#### Lancement du Backend

```bash
# Depuis la racine du projet
uvicorn backend.api.main:app --reload --port 8000

# Ou avec les variables d'environnement
SECRET_KEY=my-secret uvicorn backend.api.main:app --reload --port 8000
```

#### Accéder à l'API

- **Documentation Swagger** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentation ReDoc** : [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Frontend (React/TypeScript)

#### Installation des Dépendances

```bash
cd frontend
npm install
```

#### Lancement du Frontend

```bash
npm start
```

Le frontend sera accessible sur [http://localhost:3000](http://localhost:3000).

#### Configuration du Proxy

Le frontend est configuré pour proxyfier les requêtes API vers le backend :

```json
// frontend/package.json
{
  "proxy": "http://localhost:8000"
}
```

Cela permet d'éviter les problèmes CORS en développement.

## 📁 Structure du Projet

```
HEXLEGIA/
├── frontend/                    # Application React
│   ├── public/                 # Fichiers statiques
│   ├── src/                    # Code source
│   │   ├── index.tsx           # Point d'entrée
│   │   ├── App.tsx             # Composant principal
│   │   ├── app/                # Composants applicatifs
│   │   ├── components/         # Composants réutilisables
│   │   ├── services/           # Services API
│   │   └── types/              # Types TypeScript
│   ├── package.json            # Dépendances
│   └── tsconfig.json           # Configuration TypeScript
│
├── backend/                    # API FastAPI
│   ├── api/                    # Routes et contrôleurs
│   │   ├── main.py             # Application FastAPI
│   │   ├── routes/             # Endpoints REST
│   │   └── middleware/         # Middlewares
│   ├── core/                   # Configuration et utilitaires
│   │   ├── config.py           # Configuration
│   │   ├── logging.py          # Logging
│   │   └── exceptions.py       # Exceptions
│   ├── engines/                # 14 moteurs spécialisés
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
│   ├── architecture.md         # Architecture
│   ├── engines.md              # Documentation des moteurs
│   ├── security.md             # Sécurité
│   └── development.md          # Guide de développement
│
├── docker/                     # Configuration Docker
│   ├── Dockerfile.backend      # Backend Dockerfile
│   ├── Dockerfile.frontend     # Frontend Dockerfile
│   └── nginx.conf              # Configuration Nginx
│
├── .env.example                # Variables d'environnement
├── docker-compose.yml          # Orchestration Docker
├── README.md                   # Documentation principale
└── requirements.txt            # Dépendances Python
```

## 📝 Conventions de Codage

### Python (Backend)

1. **Nommage** :
   - Variables et fonctions : `snake_case`
   - Classes : `PascalCase`
   - Constantes : `UPPER_SNAKE_CASE`
   - Fichiers : `snake_case.py`

2. **Typage** :
   - Utiliser les **type hints** pour toutes les fonctions
   - Utiliser `Optional` pour les paramètres optionnels
   - Utiliser `Dict`, `List`, `Any` depuis `typing`

3. **Documentation** :
   - Utiliser des **docstrings** pour toutes les fonctions et classes
   - Suivre le format Google ou NumPy
   - Documenter les paramètres et retours

4. **Gestion des erreurs** :
   - Utiliser les **exceptions personnalisées**
   - Ne pas utiliser d'exceptions génériques
   - Toujours logger les erreurs

5. **Logging** :
   - Utiliser `structlog` pour le logging
   - Toujours inclure un `request_id` dans les logs
   - Utiliser les niveaux de log appropriés

**Exemple :**
```python
from typing import Optional, Dict, Any
from backend.core.logging import logger

class UserService:
    """Service pour la gestion des utilisateurs."""
    
    def __init__(self, repository: UserRepository):
        """
        Initialiser le service.
        
        Args:
            repository: Repository pour l'accès aux données.
        """
        self.repository = repository
        logger.info("UserService initialized")
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtenir un utilisateur par son ID.
        
        Args:
            user_id: ID de l'utilisateur.
        
        Returns:
            Optional[Dict[str, Any]]: Les données de l'utilisateur ou None.
        """
        try:
            user = await self.repository.get_by_id(user_id)
            logger.info("User retrieved", user_id=user_id)
            return user
        except Exception as e:
            logger.error("Failed to get user", user_id=user_id, error=str(e))
            raise
```

### TypeScript (Frontend)

1. **Nommage** :
   - Variables et fonctions : `camelCase`
   - Classes et interfaces : `PascalCase`
   - Constantes : `UPPER_SNAKE_CASE`
   - Fichiers : `kebab-case.tsx` ou `PascalCase.tsx`

2. **Typage** :
   - Utiliser les **interfaces** pour les types complexes
   - Utiliser les **types** pour les unions et alias
   - Éviter `any` autant que possible

3. **Composants React** :
   - Utiliser des **composants fonctionnels**
   - Utiliser les **hooks** pour la gestion de l'état
   - Suivre les conventions React

4. **Props** :
   - Toujours typer les props
   - Utiliser des interfaces pour les props complexes

**Exemple :**
```tsx
import React, { useState, useEffect } from 'react';

interface User {
  id: string;
  username: string;
  email: string;
  isActive: boolean;
}

interface UserCardProps {
  user: User;
  onSelect?: (userId: string) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onSelect }) => {
  const [isSelected, setIsSelected] = useState(false);

  useEffect(() => {
    // Effet de bord
  }, [user]);

  const handleClick = () => {
    setIsSelected(!isSelected);
    onSelect?.(user.id);
  };

  return (
    <div onClick={handleClick}>
      <h3>{user.username}</h3>
      <p>{user.email}</p>
      <p>Status: {user.isActive ? 'Active' : 'Inactive'}</p>
    </div>
  );
};

export default UserCard;
```

### Fichiers

1. **Encodage** : UTF-8
2. **Fin de ligne** : LF (pas CRLF)
3. **Indentation** : 4 espaces (pas de tabulations)
4. **Longueur des lignes** : 100 caractères maximum
5. **Ordre des imports** :
   - Imports standard (Python)
   - Imports tiers (bibliothèques)
   - Imports locaux (projet)

## 🧪 Tests

### Backend (Python/Pytest)

#### Structure des Tests

```
tests/
├── unit/                   # Tests unitaires
│   ├── test_health.py     # Tests pour /health
│   ├── test_engines.py    # Tests pour les moteurs
│   └── test_security.py   # Tests pour la sécurité
├── integration/            # Tests d'intégration
└── security/               # Tests de sécurité
```

#### Exemple de Test Unitaire

```python
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
```

#### Exécuter les Tests

```bash
# Exécuter tous les tests
pytest

# Exécuter avec couverture
pytest --cov=backend tests/

# Exécuter un fichier spécifique
pytest tests/unit/test_health.py

# Exécuter avec verbose
pytest -v

# Exécuter seulement les tests marqués
pytest -m slow
```

### Frontend (Jest/React Testing Library)

#### Exemple de Test de Composant

```tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import UserCard from './UserCard';

const mockUser = {
  id: '1',
  username: 'John Doe',
  email: 'john@example.com',
  isActive: true,
};

describe('UserCard', () => {
  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('Status: Active')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const mockOnSelect = jest.fn();
    render(<UserCard user={mockUser} onSelect={mockOnSelect} />);
    
    fireEvent.click(screen.getByText('John Doe'));
    expect(mockOnSelect).toHaveBeenCalledWith('1');
  });
});
```

#### Exécuter les Tests Frontend

```bash
cd frontend
npm test

# Avec couverture
npm run test:coverage
```

## 📦 Gestion des Dépendances

### Backend (Python)

```bash
# Installer une nouvelle dépendance
pip install package_name

# Installer une dépendance de développement
pip install -D package_name

# Mettre à jour les dépendances
pip install --upgrade package_name

# Générer requirements.txt
pip freeze > backend/requirements.txt
```

### Frontend (Node.js)

```bash
cd frontend

# Installer une nouvelle dépendance
npm install package_name

# Installer une dépendance de développement
npm install -D package_name

# Mettre à jour les dépendances
npm update package_name

# Vérifier les vulnérabilités
npm audit
```

## 🐳 Docker

### Commandes Utiles

```bash
# Lister les conteneurs
docker ps

# Lister tous les conteneurs (y compris arrêtés)
docker ps -a

# Voir les logs d'un conteneur
docker logs container_name

# Exécuter une commande dans un conteneur
docker exec -it container_name bash

# Arrêter un conteneur
docker stop container_name

# Démarrer un conteneur
docker start container_name

# Supprimer un conteneur
docker rm container_name

# Supprimer les images inutilisées
docker image prune

# Supprimer les volumes inutilisés
docker volume prune
```

### Docker Compose

```bash
# Lancer les services
docker-compose up -d

# Lancer avec rebuild
docker-compose up -d --build

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend

# Exécuter une commande dans un service
docker-compose exec backend bash

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

## 🔧 Outils de Développement

### Linting et Formattage

#### Backend

```bash
# Linting avec flake8
pip install flake8
flake8 backend/

# Formattage avec black
pip install black
black backend/

# Formattage avec isort
pip install isort
isort backend/
```

#### Frontend

```bash
cd frontend

# Linting avec ESLint
npm run lint

# Formattage avec Prettier
npm run format
```

### Debugging

#### Backend

```bash
# Debugging avec pdb
python -m pdb backend/api/main.py

# Debugging avec breakpoints
import pdb; pdb.set_trace()

# Debugging avec VS Code
# Créer un fichier .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["backend.api.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

#### Frontend

```bash
# Debugging avec Chrome DevTools
npm start

# Ouvrir Chrome et aller sur http://localhost:3000
# Appuyer sur F12 pour ouvrir les DevTools

# Debugging avec VS Code
# Créer un fichier .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome against localhost",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend"
    }
  ]
}
```

## 📊 Monitoring et Logging

### Logging

HexLegIA utilise `structlog` pour le logging structuré.

**Niveaux de log :**
- `DEBUG` : Informations détaillées pour le debugging
- `INFO` : Informations générales sur le fonctionnement
- `WARNING` : Avertissements pour les situations potentiellement problématiques
- `ERROR` : Erreurs qui doivent être investiguées
- `CRITICAL` : Erreurs critiques qui nécessitent une action immédiate

**Exemple de logging :**
```python
from backend.core.logging import logger

# Log simple
logger.info("Application started")

# Log avec contexte
logger.info("User logged in", user_id="123", username="john.doe")

# Log avec exception
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", error=str(e), user_id="123")
```

### Monitoring

**Métriques à monitorer :**
- Temps de réponse des endpoints
- Nombre de requêtes par minute
- Taux d'erreur
- Utilisation de la mémoire
- Utilisation du CPU
- Connexions à la base de données

**Outils recommandés :**
- **Prometheus** : Collecte de métriques
- **Grafana** : Visualisation des métriques
- **ELK Stack** : Logging centralisé
- **Sentry** : Monitoring des erreurs

## 🤝 Contribution

### Processus de Contribution

1. **Forker le dépôt** sur GitHub
2. **Cloner votre fork** localement
3. **Créer une branche** pour votre fonctionnalité :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
4. **Commiter vos changements** :
   ```bash
   git commit -m "Ajout de ma fonctionnalite"
   ```
5. **Pousser vers votre fork** :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
6. **Ouvrir une Pull Request** vers le dépôt principal

### Règles de Contribution

1. **Suivre les conventions de codage**
2. **Écrire des tests** pour les nouvelles fonctionnalités
3. **Mettre à jour la documentation** si nécessaire
4. **Ne pas committer de secrets**
5. **Garder les commits atomiques** (un commit = une fonctionnalité)
6. **Écrire des messages de commit clairs**
7. **Passer les tests CI** avant de pousser

### Revue de Code

Toutes les Pull Requests doivent être **revues** avant d'être mergées.

**Critères de revue :**
- Le code suit les conventions
- Les tests sont complets
- La documentation est à jour
- Aucune vulnérabilité de sécurité
- Le code est performant
- Le code est maintenable

## 🚨 Gestion des Problèmes

### Signaler un Bug

1. **Vérifier que le bug n'est pas déjà signalé**
2. **Créer une issue** sur GitHub avec :
   - Un titre clair et descriptif
   - Une description détaillée du problème
   - Les étapes pour reproduire le bug
   - Le comportement attendu
   - Le comportement actuel
   - Les logs ou erreurs pertinentes
   - Votre environnement (OS, versions, etc.)

### Proposer une Fonctionnalité

1. **Vérifier que la fonctionnalité n'est pas déjà proposée**
2. **Créer une issue** sur GitHub avec :
   - Un titre clair
   - Une description détaillée de la fonctionnalité
   - Les avantages de cette fonctionnalité
   - Les cas d'utilisation
   - Les éventuelles alternatives

## 📚 Ressources

### Documentation

- [Documentation principale](README.md)
- [Architecture](architecture.md)
- [Moteurs](engines.md)
- [Sécurité](security.md)

### Outils

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

### Communautés

- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [React GitHub](https://github.com/facebook/react)
- [Docker Community](https://www.docker.com/community)

## 🎯 Bonnes Pratiques

### Développement

1. **Écrire du code lisible** et maintenable
2. **Commenter votre code** lorsque nécessaire
3. **Écrire des tests** pour toutes les fonctionnalités
4. **Valider les entrées** utilisateur
5. **Gérer les erreurs** de manière appropriée
6. **Logger les opérations** importantes
7. **Respecter les interfaces** définies
8. **Éviter les dépendances inutiles**

### Sécurité

1. **Ne jamais committer de secrets**
2. **Valider toutes les entrées** utilisateur
3. **Utiliser des requêtes paramétrées** pour la base de données
4. **Gérer les erreurs** sans exposer d'informations sensibles
5. **Utiliser HTTPS** en production
6. **Mettre à jour régulièrement** les dépendances
7. **Effectuer des audits de sécurité**

### Performance

1. **Éviter les requêtes N+1**
2. **Utiliser le caching** lorsque approprié
3. **Optimiser les requêtes** à la base de données
4. **Limiter les payloads** des API
5. **Utiliser la pagination** pour les listes
6. **Minimiser les appels externes**

## 📅 Feuille de Route

### Court Terme (1-3 mois)

- [ ] Finaliser l'intégration entre les moteurs
- [ ] Implémenter la logique métier des moteurs critiques
- [ ] Ajouter des tests complets
- [ ] Configurer le CI/CD
- [ ] Déployer en environnement de staging

### Moyen Terme (3-6 mois)

- [ ] Implémenter tous les moteurs
- [ ] Ajouter l'authentification JWT complète
- [ ] Intégrer Qdrant pour la recherche vectorielle
- [ ] Développer l'interface utilisateur complète
- [ ] Déployer en production

### Long Terme (6-12 mois)

- [ ] Ajouter le support des microservices
- [ ] Implémenter l'event sourcing
- [ ] Ajouter le support GraphQL
- [ ] Développer des fonctionnalités avancées
- [ ] Optimiser les performances

## 📞 Support

Pour toute question ou problème, vous pouvez :

1. **Consulter la documentation**
2. **Créer une issue** sur GitHub
3. **Contacter l'équipe** technique

## 📄 Licence

Ce projet est propriétaire de Franck-techcell. Tous droits réservés.

## 🙏 Remerciements

Merci à tous les contributeurs qui ont participé au développement de HexLegIA !
