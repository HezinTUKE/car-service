from unittest.mock import patch, AsyncMock

import pytest
import boto3
from moto import mock_aws
from fastapi.testclient import TestClient

from application.configs import settings
from application.enums.groups import Groups
from application.main import app
from application.utils.cognito_service import CognitoService


@pytest.fixture()
def api_client():
    with mock_aws():
        cognito = boto3.client("cognito-idp", region_name=settings.AWS_REGION)

        pool = cognito.create_user_pool(PoolName="TestPool")
        pool_id = pool["UserPool"]["Id"]

        app_client = cognito.create_user_pool_client(
            UserPoolId=pool_id,
            ClientName="TestClient",
            ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
        )
        client_id = app_client["UserPoolClient"]["ClientId"]

        for group in Groups:
            cognito.create_group(
                UserPoolId=pool_id,
                GroupName=group.value,
            )

        with patch("application.utils.cognito_service.CognitoService.app_client_id", client_id), \
             patch("application.utils.cognito_service.CognitoService.user_pool_id", pool_id), \
             patch.object(CognitoService, "get_secret_hash", return_value="fakehash"), \
             patch("application.events.event.get_rabbit_processor", new_callable=AsyncMock) as mock_rabbit:

            mock_rabbit.return_value.listen = AsyncMock()

            with TestClient(app) as client:
                yield client