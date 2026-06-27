import os
from dataclasses import dataclass
from src.secrets import get_secret

@dataclass(frozen=True)
class Settings:
    db_url: str
    port: int
    transport: str
    db_pool_size: int
    db_max_overflow: int
    db_pool_recycle: int
    redis_url: str
    log_level: str
    log_json: bool
    allowed_hosts: list[str]

def load() -> Settings:
    return Settings(
        # db_url/redis_url carry credentials, so they're resolved via Secret Manager in GCP
        db_url=get_secret("SNOONU_DB_URL", "postgresql://snoonu:snoonu@localhost:5432/snoonu_mcp"),
        port=int(os.environ.get("SNOONU_MCP_PORT", "8000")),
        transport=os.environ.get("SNOONU_MCP_TRANSPORT", "streamable-http"),
        db_pool_size=int(os.environ.get("SNOONU_DB_POOL_SIZE", "10")),
        db_max_overflow=int(os.environ.get("SNOONU_DB_MAX_OVERFLOW", "20")),
        db_pool_recycle=int(os.environ.get("SNOONU_DB_POOL_RECYCLE", "1800")),
        redis_url=get_secret("SNOONU_REDIS_URL", "redis://localhost:6379/0"),
        log_level=os.environ.get("SNOONU_LOG_LEVEL", "INFO"),
        log_json=os.environ.get("SNOONU_LOG_JSON", "true").lower() == "true",
        # MCP's built-in DNS-rebinding protection only allows localhost by default;
        # deployed hosts (e.g. the Cloud Run hostname) must be added explicitly.
        allowed_hosts=[
            h.strip() for h in os.environ.get(
                "SNOONU_ALLOWED_HOSTS", "127.0.0.1:*,localhost:*,[::1]:*"
            ).split(",") if h.strip()
        ],
    )

settings = load()
