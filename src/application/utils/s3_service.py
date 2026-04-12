import os.path
from io import BytesIO

from loguru import logger
from boto3 import Session
from boto3.s3.transfer import TransferConfig
from boto3.exceptions import S3UploadFailedError
from fastapi import UploadFile

from application.utils.exceptions import BadRequestException, ServerException


class S3Service:
    bucket_name: str = "car-service-cs"
    chunk_size: int = 1024 * 1024 * 5
    file_max_size: int = 1024 * 1024 * 5

    def __init__(self, allowed_extensions: tuple = None):
        session = Session(profile_name="own")
        self.client = session.client("s3")
        self.allowed_extensions = allowed_extensions

    async def upload_file_to_s3(self, file: UploadFile, prefix: list[str], file_name: str) -> bool:
        if not file.filename.lower().endswith(self.allowed_extensions):
            raise BadRequestException(f"File type {file.content_type} is not allowed. Allowed types: {', '.join(self.allowed_extensions)}")

        if file.size > self.file_max_size:
            raise BadRequestException(f"File size must be less than {self.file_max_size} bytes")

        transfer_config = TransferConfig(
            multipart_threshold=self.chunk_size,
            multipart_chunksize=self.file_max_size,
            max_concurrency=20,
        )

        try:
            file_bytes = await file.read()
            file_extension = file.filename.split(".")[-1]
            file_name = f"{file_name}.{file_extension}"

            res = self.client.upload_fileobj(
                Fileobj=BytesIO(file_bytes),
                Bucket=self.bucket_name,
                Key=os.path.join(*prefix, file_name),
                Config=transfer_config,
            )

            return True
        except S3UploadFailedError:
            logger.exception("Error uploading file", exc_info=True)
            raise ServerException("Failed to upload file")

    async def generate_persist_url(self, prefix: list[str], file_name: str, expiration: int = 3600) -> str:
        try:
            url = self.client.generate_presigned_url(
                ClientMethod="get_object",
                ExpiresIn=expiration,
                Params={
                    "Bucket": self.bucket_name,
                    "Key": os.path.join(*prefix, file_name),
                },
            )
            return url
        except Exception:
            logger.exception("Error generating presigned URL", exc_info=True)
            raise ServerException("Failed to generate presigned URL")
