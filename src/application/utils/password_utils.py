import uuid
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv

from application.controllers import LOGIN_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/{LOGIN_CONTROLLER_PREFIX}/signin", refreshUrl=f"/{LOGIN_CONTROLLER_PREFIX}/refresh"
)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72


def get_current_user(token: str = Depends(oauth2_scheme)) -> JwtDC:
    try:
        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        permission: str = payload.get("permission")
        user_id: str = payload.get("user_id")
        jti: str = payload.get("jti")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return JwtDC(username=email, permission=Roles(permission), user_id=user_id, jti=jti)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_token(data: dict, refresh_token: bool = False):
    data["jti"] = str(uuid.uuid4())

    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    token_expires = os.getenv("TOKEN_EXPIRE_MINUTES", 30)
    refresh_token_expires = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60)

    token_expiration = token_expires if not refresh_token else refresh_token_expires

    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=token_expiration)
    to_encode["type"] = "access" if not refresh_token else "refresh"
    return jwt.encode(to_encode, key=secret_key, algorithm=algorithm)


def permission_required(allowed_roles: tuple[Roles, ...]):
    async def processor(current_user: JwtDC = Depends(get_current_user)):
        jwt_dc = current_user
        if jwt_dc.permission not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return processor
