import boto3
from datetime import datetime, timedelta, timezone

s3_client = boto3.client("s3")

BUCKET_NAME = "aws-lambda-cleanup-demo-rashmi"

# Production value
AGE_LIMIT_DAYS = 30


def lambda_handler(event, context):

    current_time = datetime.now(timezone.utc)

    paginator = s3_client.get_paginator("list_objects_v2")

    deleted_objects = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            object_key = obj["Key"]
            last_modified = obj["LastModified"]

            age = current_time - last_modified

            if age > timedelta(days=AGE_LIMIT_DAYS):

                s3_client.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=object_key
                )

                print(f"Deleted object: {object_key}")

                deleted_objects.append(object_key)


    if not deleted_objects:
        print("No objects older than 30 days found.")


    return {
        "statusCode": 200,
        "deletedObjects": deleted_objects
    }