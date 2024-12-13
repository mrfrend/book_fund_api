import jwt
import bcrypt
import datetime
from config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    # expires_minutes: int = settings.auth_jwt.auth_token_expire_minutes,
    # expires_delta: timedelta | None = None,
):

    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    # if expires_delta:
    #     expire = now + expires_delta
    # else:
    #     expire = now + datetime.timedelta(minutes=expires_minutes)
    to_encode.update(iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    ps_bytes = password.encode()
    hashed_password = bcrypt.hashpw(ps_bytes, salt)
    return hashed_password


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=hashed_password)
