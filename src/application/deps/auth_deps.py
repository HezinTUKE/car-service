import os
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import jwt
from dotenv import load_dotenv
import requests
from loguru import logger

from application.dto.jwt_dc import JwtDC
from application.enums.groups import Groups

load_dotenv()

security = HTTPBearer()
jwks = requests.get(os.getenv("AWS_COGNITO_SIGNING_KEY_URL")).json()


def verify_token(token: str):
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    app_client_id= os.getenv("AWS_COGNITO_APP_CLIENT_ID")
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

    if not key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        payload = jwt.decode(
            token=token,
            key=key,
            algorithms=["RS256"],
            audience=app_client_id,
            issuer=os.getenv("AWS_COGNITO_ISSUER")
        )
        token_use = payload.get("token_use")

        if token_use == "access":
            payload["access_token"] = token
            if payload.get("client_id") != app_client_id:
                raise HTTPException(status_code=401, detail="Invalid client_id")

        elif token_use == "id":
            if payload.get("aud") != app_client_id:
                raise HTTPException(status_code=401, detail="Invalid audience")

        return JwtDC(
            email=payload.get("email", None),
            user_id=payload["sub"],
            token=token,
            token_type=token_use,
            groups=payload.get("cognito:groups", [Groups.USER.value])
        )
    except Exception:
        logger.exception("Token verification failed", exc_info=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(credential: Annotated[HTTPBearer, Depends(security)]):
    payload = credential.credentials
    return verify_token(payload)


def require_groups(allowed_groups: tuple):
    def dependency(jwt_dc=Depends(get_current_user)):
        if not any(group.value in jwt_dc.groups for group in allowed_groups):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return jwt_dc
    return dependency
