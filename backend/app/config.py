from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    sqlite_path: str = "./data/waterwall.sqlite"

    lm_studio_base_url: str = "http://localhost:1234"
    lm_studio_api_key: str = "lm-studio"
    lm_studio_model: str = "qwen2.5-3b-instruct"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "waterwall_messages"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j_dev_password"

    daily_llm_token_budget: int = 50_000
    max_context_messages: int = 25
    summary_batch_size: int = 50
    llm_priority_threshold: float = 0.7


settings = Settings()
