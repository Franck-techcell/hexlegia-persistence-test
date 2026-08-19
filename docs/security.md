# HexLegIA - Sécurité

## 🔒 Introduction

La sécurité est un **composant critique** de HexLegIA. L'architecture a été conçue avec la sécurité comme priorité absolue, en suivant le principe de **défense en profondeur** (Defense in Depth).

## 🛡️ Principes de Sécurité

### 1. Principe du Moindre Privilège

Chaque composant, utilisateur ou service ne doit avoir que les permissions **strictement nécessaires** pour accomplir sa tâche.

### 2. Défense en Profondeur

Plusieurs couches de sécurité sont mises en place :
- Authentification
- Autorisation
- Validation des entrées
- Contrôle d'accès
- Audit
- Chiffrement

### 3. Fail-Secure

En cas d'erreur ou de défaillance, le système doit **refuser l'accès par défaut** plutôt que de l'autoriser.

### 4. Transparence

Toutes les opérations sensibles doivent être **traçables et auditable**.

### 5. Séparation des Responsabilités

Les différentes couches de sécurité sont séparées :
- **Authentification** : Qui es-tu ?
- **Autorisation** : Que peux-tu faire ?
- **Audit** : Que as-tu fait ?

## 🏗️ Architecture de Sécurité

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        Authentication                                │  │
│  │  - JWT Token Validation                                              │  │
│  │  - User Credentials Verification                                     │  │
│  │  - Session Management                                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        Authorization                                 │  │
│  │  ┌─────────────────────────────────────────────────────────────┐│  │
│  │  │                    AccessDecisionEngine                         ││  │
│  │  │  - Identity Verification                                         ││  │
│  │  │  - Requester Type Check                                           ││  │
│  │  │  - Resource & Action Validation                                   ││  │
│  │  │  - Context Analysis                                               ││  │
│  │  │  - Sensitivity Level Check                                        ││  │
│  │  │  - Policy Evaluation (RBAC/ABAC)                                 ││  │
│  │  │  - Decision & Reason Generation                                   ││  │
│  │  │  - Audit Trail Creation                                           ││  │
│  │  └─────────────────────────────────────────────────────────────┘│  │
│  │                                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────┐│  │
│  │  │                    Policies                                        ││  │
│  │  │  - RBAC: Role-Based Access Control                              ││  │
│  │  │  - ABAC: Attribute-Based Access Control                         ││  │
│  │  │  - Custom Policies                                               ││  │
│  │  └─────────────────────────────────────────────────────────────┘│  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        Audit                                          │  │
│  │  - Request Logging                                                   │  │
│  │  - Decision Logging                                                  │  │
│  │  - Action Logging                                                    │  │
│  │  - Error Logging                                                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔐 Authentification

### JWT (JSON Web Tokens)

HexLegIA utilise **JWT** pour l'authentification stateless.

**Avantages :**
- Stateless (pas de session serveur)
- Scalable
- Sécurisé (avec des clés fortes)
- Standardisé

**Configuration :**
```python
# backend/core/config.py
class Settings(BaseSettings):
    secret_key: str = "change-me-in-production-for-jwt-signing"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

**⚠️ IMPORTANT :** La `secret_key` doit être **changée en production** et ne doit **jamais être committée** dans le dépôt.

### Processus d'Authentification

```
1. Utilisateur soumet ses credentials (username/password)
2. Backend vérifie les credentials
3. Si valides, backend génère un JWT
4. JWT est retourné au client
5. Client stocke le JWT (localStorage, cookies, etc.)
6. Pour chaque requête, client envoie le JWT dans le header Authorization
7. Backend valide le JWT
8. Si valide, backend extrait les informations utilisateur
9. Requête est traitée
```

### Middleware d'Authentification

```python
# backend/api/middleware/security.py
from fastapi import Request, HTTPException, status
from jose import JWTError, jwt
from backend.core.config import settings

async def authenticate_request(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )
    
    try:
        payload = jwt.decode(
            token.split(" ")[1],
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

## 🔑 Autorisation

### AccessDecisionEngine

**⚠️ COMPOSANT CRITIQUE**

Le **AccessDecisionEngine** est le **point de contrôle centralisé** pour toutes les décisions d'accès dans HexLegIA.

**Règle Absolue :**
> Aucun service manipulant une donnée sensible ou exécutant une action protégée ne doit pouvoir contourner ce mécanisme.

### Principe de Fonctionnement

```
Utilisateur / IA
       ↓
Authentification (JWT)
       ↓
ACCESS DECISION ENGINE
       ↓
   ┌─────────────────────┐
   │ Vérification :       │
   │ - Identité           │
   │ - Type de demandeur  │
   │ - Ressource          │
   │ - Action             │
   │ - Contexte           │
   │ - Justification      │
   │ - Niveau sensibilité │
   └─────────────────────┘
       ↓
   ┌─────────────────────┐
   │ Évaluation :        │
   │ - Politiques RBAC   │
   │ - Politiques ABAC   │
   │ - Règles personnal.  │
   └─────────────────────┘
       ↓
   ┌─────────────────────┐
   │ Décision :          │
   │ - Autorisé ?        │
   │ - Raison            │
   │ - Trace d'audit     │
   └─────────────────────┘
       ↓
   ┌─────────┐ ┌─────────┐
   │  OUI    │ │  NON    │
   │ Accès   │ │ Refus   │
   │ autorisé│ │ (403)   │
   └─────────┘ └─────────┘
```

### Contrat du AccessDecisionEngine

Chaque requête d'accès doit fournir :

| Élément | Type | Description | Obligatoire |
|--------|------|-------------|-------------|
| `requester` | str | Identité du demandeur | ✅ |
| `requester_type` | RequesterType | Type du demandeur (HUMAN, AI, SERVICE, SYSTEM) | ✅ |
| `resource` | str | Ressource demandée (URL, identifiant, etc.) | ✅ |
| `action` | str | Action demandée (GET, POST, DELETE, etc.) | ✅ |
| `context` | Dict[str, Any] | Contexte supplémentaire | ❌ |
| `justification` | str | Justification de la requête | ❌ |
| `sensitivity_level` | SensitivityLevel | Niveau de sensibilité (PUBLIC, INTERNAL, CONFIDENTIAL, SECRET) | ✅ |

La réponse contient :

| Élément | Type | Description |
|--------|------|-------------|
| `allowed` | bool | Si l'accès est autorisé |
| `decision` | DecisionType | Type de décision (ALLOWED, DENIED, PENDING, CONDITIONAL) |
| `reason` | str | Raison de la décision |
| `justification` | str | Justification de la décision |
| `conditions` | List[str] | Conditions pour l'accès |
| `policies_applied` | List[str] | Politiques appliquées |
| `audit_trace` | Dict[str, Any] | Trace d'audit |
| `confidence_score` | float | Score de confiance (0-1) |

### Politiques d'Autorisation

#### RBAC (Role-Based Access Control)

Basé sur les **rôles** des utilisateurs.

**Exemple :**
```python
# Définition des rôles
admin_role = {
    "name": "admin",
    "permissions": {
        "*": ["*"],  # Tous les accès
    },
}

user_role = {
    "name": "user",
    "permissions": {
        "/api/data": ["GET"],
        "/api/profile": ["GET", "PUT"],
    },
}

# Assignation des rôles
user_roles = {
    "user_1": ["admin"],
    "user_2": ["user"],
}
```

**Avantages :**
- Simple à comprendre et à maintenir
- Efficace pour les structures hiérarchiques
- Performant

**Limites :**
- Peu flexible pour les cas complexes
- Difficile à adapter aux changements

#### ABAC (Attribute-Based Access Control)

Basé sur les **attributs** du demandeur, de la ressource et du contexte.

**Exemple :**
```python
# Définition des règles ABAC
rules = [
    {
        "name": "access_during_working_hours",
        "condition": lambda requester_attrs, resource_attrs, context: (
            context.get("hour") >= 9 and context.get("hour") <= 17
        ),
        "effect": "allow",
        "description": "Accès autorisé entre 9h et 17h",
    },
    {
        "name": "access_from_secure_location",
        "condition": lambda requester_attrs, resource_attrs, context: (
            requester_attrs.get("ip") in SECURE_IPS
        ),
        "effect": "allow",
        "description": "Accès autorisé depuis les IP sécurisées",
    },
]
```

**Avantages :**
- Très flexible
- Adaptable aux cas complexes
- Granulaire

**Limites :**
- Plus complexe à configurer
- Peut être moins performant

### Niveaux de Sensibilité

Les ressources peuvent être classées selon leur niveau de sensibilité :

| Niveau | Description | Exemples |
|-------|-------------|----------|
| PUBLIC | Données publiques | Documentation, informations générales |
| INTERNAL | Données internes | Rapports internes, processus métiers |
| CONFIDENTIAL | Données confidentielles | Données clients, contrats |
| SECRET | Données secrètes | Secrets commerciaux, stratégies |
| TOP_SECRET | Données ultra-sensibles | Données gouvernementales, secrets d'État |

## 📝 Audit

### Mécanisme d'Audit

Chaque opération importante est tracée avec les informations suivantes :

| Élément | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Date et heure de l'opération |
| `request_id` | str | ID unique de la requête |
| `requester` | str | Identité du demandeur |
| `requester_type` | RequesterType | Type du demandeur |
| `resource` | str | Ressource concernée |
| `action` | str | Action effectuée |
| `decision` | DecisionType | Décision prise |
| `result` | str | Résultat de l'opération |
| `reason` | str | Raison de la décision |
| `metadata` | Dict[str, Any] | Métadonnées supplémentaires |

### Exemple de Trace d'Audit

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_abc123",
  "requester": "user_123",
  "requester_type": "HUMAN",
  "resource": "/api/admin/users",
  "action": "GET",
  "decision": "DENIED",
  "result": "403 Forbidden",
  "reason": "User does not have admin role",
  "metadata": {
    "policies_applied": ["default_deny", "admin_only"],
    "user_roles": ["user"],
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
}
```

### Stockage des Logs d'Audit

Les logs d'audit sont stockés :
1. **Dans un fichier** : Pour consultation locale
2. **Dans la base de données** : Pour analyse et reporting
3. **Dans un système externe** : Pour archivage long terme (optionnel)

**Configuration :**
```python
# backend/core/config.py
class Settings(BaseSettings):
    audit_enabled: bool = True
    audit_log_file: str = "/var/log/hexlegia/audit.log"
```

### Middleware d'Audit

```python
# backend/api/middleware/audit.py
async def audit_middleware(request: Request, call_next):
    # Capturer les informations de la requête
    audit_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": request.state.request_id,
        "method": request.method,
        "path": request.url.path,
        "client": {
            "host": request.client.host,
            "port": request.client.port,
        },
    }
    
    # Exécuter la requête
    response = await call_next(request)
    
    # Capturer les informations de la réponse
    audit_data["status_code"] = response.status_code
    
    # Écrire dans le log d'audit
    _write_audit_log(audit_data)
    
    return response
```

## 🔧 Configuration de Sécurité

### Variables d'Environnement

```bash
# backend/.env.example

# JWT Configuration
SECRET_KEY=change-me-in-production-for-jwt-signing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Audit Configuration
AUDIT_ENABLED=true
AUDIT_LOG_FILE=/var/log/hexlegia/audit.log
```

### Bonnes Pratiques de Configuration

1. **Ne jamais committer de secrets** dans le dépôt
2. **Utiliser des variables d'environnement** pour les configurations sensibles
3. **Changer les clés par défaut** en production
4. **Limiter les origines CORS** aux domaines autorisés
5. **Activer l'audit** en production
6. **Configurer des timeouts** pour les requêtes

## 🛡️ Protection contre les Attaques Courantes

### 1. Injection SQL

**Protection :**
- Utilisation de **SQLAlchemy ORM** (pas de SQL brut)
- Utilisation de **paramètres préparés** pour les requêtes SQL
- Validation des entrées avec **Pydantic**

**Exemple vulnérable :**
```python
# ❌ À NE PAS FAIRE
user_id = request.query_params.get("user_id")
query = f"SELECT * FROM users WHERE id = {user_id}"  # Injection possible
```

**Exemple sécurisé :**
```python
# ✅ À FAIRE
user_id = request.query_params.get("user_id")
query = "SELECT * FROM users WHERE id = :user_id"
result = await db.execute(query, {"user_id": user_id})
```

### 2. Cross-Site Scripting (XSS)

**Protection :**
- **Échappement automatique** avec React
- **Content Security Policy (CSP)** headers
- **Validation des entrées** utilisateur

**Headers de sécurité :**
```python
# backend/api/middleware/security.py
response.headers["X-Frame-Options"] = "SAMEORIGIN"
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-XSS-Protection"] = "1; mode=block"
response.headers["Content-Security-Policy"] = "default-src 'self'"
```

### 3. Cross-Site Request Forgery (CSRF)

**Protection :**
- **JWT dans les headers** (pas dans les cookies)
- **SameSite cookies** si cookies utilisés
- **CSRF tokens** pour les formulaires

### 4. Denial of Service (DoS)

**Protection :**
- **Rate limiting** sur les endpoints sensibles
- **Timeouts** sur les requêtes
- **Limitation de la taille** des payloads

**Configuration du rate limiting :**
```python
# backend/core/config.py
class Settings(BaseSettings):
    rate_limit_requests: int = 100  # 100 requêtes
    rate_limit_period: int = 60    # par minute
```

### 5. Man-in-the-Middle (MITM)

**Protection :**
- **HTTPS obligatoire** en production
- **HSTS header** pour forcer HTTPS
- **Certificats valides** et à jour

**Header HSTS :**
```python
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
```

## 🔐 Gestion des Secrets

### Bonnes Pratiques

1. **Ne jamais stocker de secrets dans le code**
2. **Utiliser des variables d'environnement**
3. **Utiliser un gestionnaire de secrets** en production (Vault, AWS Secrets Manager, etc.)
4. **Rotater les secrets régulièrement**
5. **Limiter l'accès aux secrets**

### Exemple de Gestion des Secrets

```python
# ❌ À NE PAS FAIRE
SECRET_KEY = "ma_cle_secrete_en_dur"  # Dans le code

# ✅ À FAIRE
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")  # Depuis l'environnement

settings = Settings()
```

### Utilisation de .env

```bash
# .env.example (à committer)
SECRET_KEY=change-me-in-production
DATABASE_URL=postgresql://user:pass@localhost/db

# .env (NE PAS COMMITTER)
SECRET_KEY=my-very-secret-key-12345
DATABASE_URL=postgresql://prod_user:prod_pass@prod-db:5432/prod_db
```

## 📊 Monitoring et Alertes

### Métriques de Sécurité

Les métriques suivantes doivent être monitorées :

- **Nombre de requêtes** par minute/heure/jour
- **Nombre de requêtes refusées** (403)
- **Nombre de requêtes non autorisées** (401)
- **Temps de réponse** moyen et maximum
- **Erreurs** par endpoint
- **Activité suspecte** (trop de requêtes, patterns anormaux)

### Alertes de Sécurité

Des alertes doivent être déclenchées pour :

- **Trop de requêtes refusées** (possible attaque)
- **Temps de réponse anormalement long** (possible DoS)
- **Erreurs répétées** (possible problème de sécurité)
- **Accès depuis des IP suspectes**
- **Comportement anormal** des utilisateurs

## 🎯 Checklist de Sécurité

### Avant le Déploiement

- [ ] Tous les secrets sont **hors du code**
- [ ] Les variables d'environnement sont **configurées**
- [ ] HTTPS est **activé** en production
- [ ] Les headers de sécurité sont **configurés**
- [ ] Le rate limiting est **activé**
- [ ] L'audit est **activé**
- [ ] Les logs sont **configurés**
- [ ] Les backups sont **configurés**
- [ ] Les tests de sécurité ont été **exécutés**

### Pour le Développement

- [ ] Ne pas utiliser de **vrais secrets** en développement
- [ ] Désactiver l'audit en développement si nécessaire
- [ ] Utiliser des **données de test**
- [ ] Ne pas exposer le backend **publiquement**

## 📚 Ressources de Sécurité

### Outils Recommandés

- **OWASP ZAP** : Scanner de vulnérabilités
- **Bandit** : Analyse de code Python pour les vulnérabilités
- **Snyk** : Détection des vulnérabilités dans les dépendances
- **Trivy** : Scanner de conteneurs Docker
- **SQLMap** : Test d'injection SQL (pour les tests de pénétration)

### Bonnes Pratiques

1. **Mettre à jour régulièrement** les dépendances
2. **Effectuer des audits de sécurité** réguliers
3. **Former les développeurs** aux bonnes pratiques de sécurité
4. **Effectuer des tests de pénétration** avant le déploiement
5. **Monitorer les vulnérabilités** connues

### Références

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)
