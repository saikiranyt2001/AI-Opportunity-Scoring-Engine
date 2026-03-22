from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Opportunity Engine"
    environment: str = "development"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://user:password@localhost/db"

    openai_url: str = "https://api.openai.com/v1"
    anthropic_url: str = "https://api.anthropic.com"
    gemini_url: str = "https://generativelanguage.googleapis.com"
    grok_url: str = "https://api.x.ai"

    scheduler_interval_hours: int = 24
    scheduler_timezone: str = "America/Chicago"
    pipeline_hour_ct: int = 5
    position_monitor_hour_ct: int = 6
    patent_scanner_weekday: str = "mon"
    patent_scanner_hour_ct: int = 7
    digest_weekday: str = "sun"
    digest_hour_ct: int = 8

    stripe_webhook_secret: str = ""
    enable_stripe_test_webhook: bool = False
    sendgrid_api_key: str = ""
    digest_default_recipient: str = "subscriber@example.com"
    digest_subject: str = "Weekly Opportunity Digest"

    # Compliance constraint: this must stay disabled with no env override.
    REDDIT_ENABLED: ClassVar[bool] = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
