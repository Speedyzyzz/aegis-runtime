from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow", env_file=".env")

    PROJECT_NAME: str = "Aegis Runtime"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///aegis.db",
        description="Database connection string (SQLite for offline tests, PostgreSQL in production)"
    )
    
    # Security perimeters
    SANDBOX_FS_ROOT: str = "/tmp/aegis_sandbox"
    AUTO_APPROVE_BLAST_RADIUS_THRESHOLD: float = 30.0  # actions with score > 30 require human approval
    DEFAULT_TOKEN_TTL_SECONDS: int = 60

settings = Settings()
