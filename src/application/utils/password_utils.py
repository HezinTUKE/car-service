from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from application import config
from application.controllers import LOGIN_CONTROLLER_NAME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{LOGIN_CONTROLLER_NAME}/signin")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        secret_key = config["security"]["secret_key"]
        algorithm = config["security"]["algorithm"]

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict, refresh_token: bool = False):
    secret_key = config["security"]["secret_key"]
    algorithm = config["security"]["algorithm"]
    token_expiration = config["security"]["token_expire"] if not refresh_token else config["security"]["refresh_token_expire"]

    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=token_expiration)
    to_encode["type"] = "access" if not refresh_token else "refresh"
    return jwt.encode(to_encode, key=secret_key, algorithm=algorithm)
