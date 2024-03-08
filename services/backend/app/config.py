from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "6d0ff6398bad6c981dc25a21c9b60ab3431f42cb0aff7a5efb77f77775208dc4"
    mini_url: str = "http://miniflux:8080"
    openai_api_key: str = "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"
    mini_api_key: str = "STR83xehCIda8SlsSOH8b5sdLY5xIUK9DlEePwDGlTU="
    pinecone_api_key: str = "60eebef1-0cde-487d-9133-b0e83eeeb61d"
    pinecone_index: str = "feeds"


settings = Settings()  # type: ignore
