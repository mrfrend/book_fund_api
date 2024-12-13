from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    auth_token_expire_minutes: int = 60


class Settings(BaseSettings):
    DB_URL: str

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///book_fund.db"

    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
