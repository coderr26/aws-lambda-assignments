import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client("ec2")

VOLUME_ID = "vol-0f17fd69c53c384d9"

RETENTION_DAYS = 30

TAG_KEY = "CreatedBy"
TAG_VALUE = "Lambda-Backup"


def lambda_handler(event, context):

    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Snapshot"
    )

    snapshot_id = snapshot["SnapshotId"]

    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                "Key": TAG_KEY,
                "Value": TAG_VALUE
            }
        ]
    )

    print(f"Created Snapshot: {snapshot_id}")

    deleted_snapshots = []

    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": f"tag:{TAG_KEY}",
                "Values": [TAG_VALUE]
            }
        ]
    )["Snapshots"]

    current_time = datetime.now(timezone.utc)

    for snap in snapshots:

        age = current_time - snap["StartTime"]

        if age > timedelta(days=RETENTION_DAYS):

            ec2.delete_snapshot(
                SnapshotId=snap["SnapshotId"]
            )

            print(f"Deleted Snapshot: {snap['SnapshotId']}")

            deleted_snapshots.append(
                snap["SnapshotId"]
            )

    return {
        "statusCode": 200,
        "createdSnapshot": snapshot_id,
        "deletedSnapshots": deleted_snapshots
    }