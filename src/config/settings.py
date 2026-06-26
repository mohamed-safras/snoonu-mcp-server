import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    db_url: str
    port: int
    transport: str

def load() -> Settings:
    return Settings(
        db_url=os.environ.get("SNOONU_DB_URL", "postgresql://snoonu:snoonu@localhost:5432/snoonu_mcp"),
        port=int(os.environ.get("SNOONU_MCP_PORT", "8000")),
        transport=os.environ.get("SNOONU_MCP_TRANSPORT", "streamable-http")
    )
    
settings = load()