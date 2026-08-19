"""
HexLegIA Health Check Route
===========================

Route de vérification de santé de l'application.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime

from backend.core.config import settings
from backend.core.logging import logger

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Vérifier l'état de santé de l'application.
    
    Returns:
        Dict[str, Any]: État de santé avec les informations de base.
    """
    logger.info("Health check requested")
    
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "debug": settings.debug,
    }


@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_health_check() -> Dict[str, Any]:
    """
    Vérification de santé détaillée avec l'état des dépendances.
    
    Returns:
        Dict[str, Any]: État détaillé de santé.
    """
    logger.info("Detailed health check requested")
    
    # Vérifier la connexion à PostgreSQL
    postgres_status = await _check_postgres()
    
    # Vérifier la connexion à Qdrant
    qdrant_status = await _check_qdrant()
    
    return {
        "status": "ok" if postgres_status and qdrant_status else "degraded",
        "app": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "debug": settings.debug,
        "dependencies": {
            "postgres": postgres_status,
            "qdrant": qdrant_status,
        },
    }


async def _check_postgres() -> Dict[str, Any]:
    """Vérifier la connexion à PostgreSQL."""
    try:
        import asyncpg
        import asyncio
        
        # Timeout de 2 secondes
        timeout = 2
        
        async def check():
            conn = await asyncpg.connect(
                user=settings.postgres_user,
                password=settings.postgres_password,
                database=settings.postgres_db,
                host=settings.postgres_host,
                port=settings.postgres_port,
            )
            await conn.close()
            return True
        
        # Exécuter avec timeout
        try:
            await asyncio.wait_for(check(), timeout=timeout)
            return {"status": "healthy", "message": "Connection successful"}
        except asyncio.TimeoutError:
            return {"status": "unhealthy", "message": "Connection timeout"}
            
    except Exception as e:
        logger.warning("PostgreSQL health check failed", error=str(e))
        return {"status": "unhealthy", "message": str(e)}


async def _check_qdrant() -> Dict[str, Any]:
    """Vérifier la connexion à Qdrant."""
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
        import httpx
        
        # Timeout de 2 secondes
        timeout = 2
        
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=timeout,
        )
        
        # Vérifier la santé
        health = client.get_health()
        
        if health.status == "healthy":
            return {"status": "healthy", "message": "Connection successful"}
        else:
            return {"status": "unhealthy", "message": health.status}
            
    except Exception as e:
        logger.warning("Qdrant health check failed", error=str(e))
        return {"status": "unhealthy", "message": str(e)}


# État du module
MODULE_STATUS = "IMPLEMENTED"
