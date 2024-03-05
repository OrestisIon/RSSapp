from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "6d0ff6398bad6c981dc25a21c9b60ab3431f42cb0aff7a5efb77f77775208dc4"
    mini_url: str = "http://miniflux:8080"
    mini_api_key: str = "xEzgfo_f3_E8kCwW3cPMdX6HIEV59AXIN8xeF8BB83U="


settings = Settings()  # type: ignore
