import os
import uuid

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

if not AWS_REGION or not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_S3_BUCKET:
    raise RuntimeError("Missing AWS S3 environment variables")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def _make_s3_key(folder: str, filename: str | None) -> str:
    ext = ""
    if filename and "." in filename:
        ext = "." + filename.rsplit(".", 1)[1].lower()

    return f"{folder.rstrip('/')}/{uuid.uuid4()}{ext}"


async def upload_file_to_s3(file: UploadFile, folder: str) -> str:
    try:
        key = _make_s3_key(folder, file.filename)

        file.file.seek(0)

        extra_args = {}
        if file.content_type:
            extra_args["ContentType"] = file.content_type

        s3_client.upload_fileobj(
            Fileobj=file.file,
            Bucket=AWS_S3_BUCKET,
            Key=key,
            ExtraArgs=extra_args,
        )

        return key

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")


def generate_presigned_download_url(key: str, expires_in: int = 3600) -> str:
    try:
        return s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": AWS_S3_BUCKET,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")