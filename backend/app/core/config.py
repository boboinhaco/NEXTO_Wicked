from pydantic_settings import BaseSettings


# .env 기반 설정
class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://nexto:nexto@localhost:5432/nexto"
    llm_api_key: str = ""
    llm_model: str = ""
    web_search_api_key: str = ""
    public_data_api_key: str = ""
    kakao_rest_api_key: str = ""
    storage_dir: str = "./uploads"
    jwt_secret: str = "change-me-please-32-bytes-minimum!!"
    demo_mode: bool = True
    cors_origins: str = "http://localhost:5173"
    job_hard_timeout_sec: int = 75

    class Config:
        env_file = ".env"


settings = Settings()
