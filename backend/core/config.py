"""
HexLegIA Configuration Module
==============================

Gestion centralisée de la configuration de l'application.
Utilise Pydantic Settings pour la validation et le typage.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Configuration principale de l'application HexLegIA."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # ========================================
    # Application Settings
    # ========================================
    app_name: str = "HexLegIA"
    app_version: str = "1.0.0"
    app_description: str = "HexLegIA Technical Foundation V1"
    debug: bool = Field(default=False, env="BACKEND_DEBUG")
    
    # ========================================
    # Server Settings
    # ========================================
    host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    port: int = Field(default=8000, env="BACKEND_PORT")
    
    # ========================================
    # PostgreSQL Settings
    # ========================================
    postgres_user: str = Field(default="hexlegia", env="POSTGRES_USER")
    postgres_password: str = Field(default="hexlegia_password", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="hexlegia_db", env="POSTGRES_DB")
    postgres_host: str = Field(default="postgres", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    
    @property
    def postgres_dsn(self) -> str:
        """DSN pour la connexion PostgreSQL."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def postgres_dsn_sync(self) -> str:
        """DSN pour la connexion PostgreSQL synchrone."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # ========================================
    # Qdrant Settings
    # ========================================
    qdrant_host: str = Field(default="qdrant", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    
    @property
    def qdrant_url(self) -> str:
        """URL pour la connexion Qdrant."""
        return f"http://{self.qdrant_host}:{self.qdrant_port}"
    
    # ========================================
    # Security Settings
    # ========================================
    secret_key: str = Field(default="change-me-in-production-for-jwt-signing", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # ========================================
    # CORS Settings
    # ========================================
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parser les origines CORS depuis une chaîne séparée par des virgules."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    # ========================================
    # Logging Settings
    # ========================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # ========================================
    # Audit Settings
    # ========================================
    audit_enabled: bool = Field(default=True, env="AUDIT_ENABLED")
    audit_log_file: str = Field(default="/var/log/hexlegia/audit.log", env="AUDIT_LOG_FILE")
    
    # ========================================
    # AI Provider Settings
    # ========================================
    mistral_api_key: Optional[str] = Field(default=None, env="MISTRAL_API_KEY")
    mistral_api_url: str = Field(default="https://api.mistral.ai/v1", env="MISTRAL_API_URL")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_api_url: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_URL")
    
    # ========================================
    # Rate Limiting Settings
    # ========================================
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_period: int = Field(default=60, env="RATE_LIMIT_PERIOD")


# Instance globale des paramètres
settings = Settings()

# Validation au démarrage
if settings.debug:
    print("⚠️  Mode DEBUG activé - Ne pas utiliser en production !")
    if settings.secret_key == "change-me-in-production-for-jwt-signing":
        print("⚠️  SECRET_KEY par défaut détecté - Changer pour la production !")
