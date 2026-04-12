import base64
import hashlib
import hmac
import os
from boto3 import Session
from debugpy.adapter import access_token
from loguru import logger
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from application.enums.roles import Roles
from application.schemas.auth_response_schemas import AuthResponseSchema

load_dotenv()


class CognitoService:
    app_client_id: str = os.getenv("AWS_COGNITO_APP_CLIENT_ID")
    app_client_secret: str = os.getenv("AWS_COGNITO_APP_CLIENT_SECRET")

    def __init__(self):
        session = Session(profile_name=os.getenv("AWS_PROFILE", "default"))
        self.client = session.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))

    def sign_up_user(self, password: str, email: str):
        try:
            response = self.client.sign_up(
                ClientId=self.app_client_id,
                Username=email,
                Password=password,
                SecretHash=self.get_secret_hash(email),
                UserAttributes=[{"Name": "email", "Value": email}],
            )
            return response
        except ClientError as e:
            logger.exception("Error signing up user", exc_info=True)
            raise e

    def add_user_to_group(self, username: str, group_name: Roles):
        try:
            response = self.client.admin_add_user_to_group(
                UserPoolId=os.getenv("AWS_USER_POOL_ID"),
                Username=username,
                GroupName=group_name.value,
            )
            return response
        except ClientError as e:
            logger.exception("Error adding user to group", exc_info=True)
            raise e

    def login_user(self, username: str, password: str):
        try:
            response = self.client.initiate_auth(
                ClientId=self.app_client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": self.get_secret_hash(username),
                },
            )
            auth = response["AuthenticationResult"]
            return AuthResponseSchema(
                access_token=auth["AccessToken"],
                refresh_token=auth["RefreshToken"],
                id_token=auth["IdToken"],
                expires_in=auth["ExpiresIn"],
                token_type=auth["TokenType"],
            )
        except ClientError as e:
            logger.exception("Error logging in user", exc_info=True)
            raise e

    def logout_user(self, access_token: str):
        try:
            response = self.client.global_sign_out(
                AccessToken=access_token
            )
            return response
        except ClientError as e:
            logger.exception("Error logging out user", exc_info=True)
            raise e

    def confirm_user(self, username: str, confirmation_code: str):
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.app_client_id,
                Username=username,
                ConfirmationCode=confirmation_code,
                SecretHash=self.get_secret_hash(username),
            )
            return response
        except ClientError as e:
            logger.exception("Error confirming user", exc_info=True)
            raise e

    def refresh_token(self, refresh_token: str):
        try:
            response = self.client.initiate_auth(
                ClientId=self.app_client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                    "SECRET_HASH": self.app_client_secret,
                },
            )
            auth = response["AuthenticationResult"]
            return AuthResponseSchema(
                access_token=auth["AccessToken"],
                refresh_token=refresh_token,
                id_token=auth["IdToken"],
                expires_in=auth["ExpiresIn"],
                token_type=auth["TokenType"],
            )
        except ClientError as e:
            logger.exception("Error refreshing token", exc_info=True)
            raise e

    def forgot_password(self, username: str):
        try:
            response = self.client.forgot_password(
                ClientId=self.app_client_id,
                Username=username,
                SecretHash=self.get_secret_hash(username),
            )
            return response
        except ClientError as e:
            logger.exception("Error initiating forgot password flow", exc_info=True)
            raise e

    def reset_password(self, username: str, confirmation_code: str, new_password: str):
        try:
            response = self.client.confirm_forgot_password(
                ClientId=self.app_client_id,
                Username=username,
                ConfirmationCode=confirmation_code,
                Password=new_password,
                SecretHash=self.get_secret_hash(username),
            )
            return response
        except ClientError as e:
            logger.exception("Error resetting password", exc_info=True)
            raise e

    def get_secret_hash(self, username: str) -> str:
        client_id = self.app_client_id

        message = username + client_id

        digest = hmac.new(
            key=self.app_client_secret.encode("utf-8"),
            msg=message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        return base64.b64encode(digest).decode()
