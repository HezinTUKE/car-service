from loguru import logger
import boto3


def handler(event, context):
    logger.info(f"Post confirmation trigger event: {event}")

    if event["triggerSource"] != "PostConfirmation_ConfirmSignUp":
        return event

    client = boto3.client("cognito-idp")

    try:
        client.admin_add_user_to_group(
            UserPoolId=event["userPoolId"],
            Username=event["userName"],
            GroupName="user",
        )
        logger.info(f"User {event['userName']} added to 'user' group")
    except Exception as e:
        logger.exception("Failed to add user to group", exc_info=True)
        raise e

    return event
