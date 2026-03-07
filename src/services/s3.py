import os
import uuid

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


def get_s3_client():
    if not AWS_REGION or not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_S3_BUCKET:
        raise HTTPException(status_code=500, detail="Missing AWS S3 environment variables")

    return boto3.client(
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


def is_s3_key(path: str | None) -> bool:
    if not path:
        return False

    valid_prefixes = (
        "employees-documents/",
        "employees-cheques/",
        "employees-police/",
        "employees-medical/",
    )
    return path.startswith(valid_prefixes)


async def upload_file_to_s3(file: UploadFile, folder: str) -> str:
    try:
        s3_client = get_s3_client()
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


def s3_object_exists(key: str) -> bool:
    try:
        s3_client = get_s3_client()
        s3_client.head_object(Bucket=AWS_S3_BUCKET, Key=key)
        return True
    except ClientError:
        return False


def safe_presigned_url(key: str | None, expires_in: int = 3600) -> str | None:
    if not key:
        return None

    if not is_s3_key(key):
        return None

    if not s3_object_exists(key):
        return None

    try:
        s3_client = get_s3_client()
        return s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": AWS_S3_BUCKET, "Key": key},
            ExpiresIn=expires_in,
        )
    except ClientError:
        return None