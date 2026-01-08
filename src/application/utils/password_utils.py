from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from starlette.responses import JSONResponse

from application import config
from application.controllers import LOGIN_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/{LOGIN_CONTROLLER_PREFIX}/signin", refreshUrl=f"/{LOGIN_CONTROLLER_PREFIX}/refresh"
)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72


def get_current_user(token: str = Depends(oauth2_scheme)) -> JwtDC:
    try:
        secret_key = config.security.secret_key
        algorithm = config.security.algorithm

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

    secret_key = config.security.secret_key
    algorithm = config.security.algorithm
    token_expiration = config.security.token_expire if not refresh_token else config.security.refresh_token_expire

    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=token_expiration)
    to_encode["type"] = "access" if not refresh_token else "refresh"
    return jwt.encode(to_encode, key=secret_key, algorithm=algorithm)


def set_token(response: JSONResponse, data: dict, refresh_token: bool = False):
    cookie_key = "refresh_token" if refresh_token else "access_token"
    access_token = create_token(data, refresh_token)
    response.set_cookie(key=cookie_key, value=access_token, httponly=True, secure=True, samesite="lax")


def permission_required(allowed_roles: tuple[Roles, ...]):
    async def processor(current_user: JwtDC = Depends(get_current_user)):
        jwt_dc = current_user
        if jwt_dc.permission not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return processor
