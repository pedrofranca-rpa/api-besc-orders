from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ✅ Usa SQLite local (arquivo database.db na raiz do projeto)
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

    # 🔒 Configurações JWT (você pode manter como está)
    JWT_SECRET: str = "%8l£cIL{h1*b}uaDgri*.O\^73I!03te(.t7P2[Z{GD-JP@'E"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
