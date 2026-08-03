import boto3
from datetime import datetime, timezone


ec2 = boto3.client("ec2")


def lambda_handler(event, context):

    print("Received Event:")
    print(event)

    instance_id = event["detail"]["instance-id"]

    current_date = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")


    tags = [
        {
            "Key": "LaunchDate",
            "Value": current_date
        },
        {
            "Key": "Environment",
            "Value": "Development"
        },
        {
            "Key": "Owner",
            "Value": "Lambda-Automation"
        }
    ]


    ec2.create_tags(
        Resources=[
            instance_id
        ],
        Tags=tags
    )


    message = (
        f"Successfully tagged instance "
        f"{instance_id}"
    )

    print(message)


    return {
        "statusCode": 200,
        "message": message,
        "instanceId": instance_id
    }