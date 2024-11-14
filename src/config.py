from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    @property
    def db_url(self):
        return f"sqlite:///book_fund.db"

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
