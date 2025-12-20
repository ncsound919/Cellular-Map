"""Configuration settings for NetworkCellularMap"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "NetworkCellularMap"
    VERSION: str = "2.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Neo4j Database
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    # WARNING: Change NEO4J_PASSWORD via environment variable before deployment
    # This default value is insecure and only for local development
    NEO4J_PASSWORD: str = "password"
    NEO4J_DATABASE: str = "neo4j"
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # External APIs
    OMIM_API_KEY: Optional[str] = None
    NCBI_API_KEY: Optional[str] = None
    KEGG_API_BASE: str = "https://rest.kegg.jp"
    
    # AI Models
    MODEL_PATH: str = "./models"
    CAUSAL_DISCOVERY_METHOD: str = "PC_stable"
    
    # Network Analysis
    HUB_DEGREE_THRESHOLD: int = 50
    HUB_BETWEENNESS_THRESHOLD: float = 0.1
    POWER_LAW_ALPHA_MIN: float = 2.1
    POWER_LAW_ALPHA_MAX: float = 2.7
    
    # CRISPR Design
    GRNA_LENGTH: int = 20
    AAV9_CAPACITY_KB: float = 4.7
    AAV9_TITER_MIN: float = 1e13
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
