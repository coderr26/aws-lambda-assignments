# Task2 - Automated EBS Snapshot Creation and Cleanup

## Objective

Automate Amazon EBS volume backups by creating snapshots using AWS Lambda and automatically remove snapshots older than a defined retention period.

The solution creates a snapshot of a specified EBS volume, adds a custom tag, identifies older snapshots created by Lambda, and deletes snapshots that exceed the retention period.

---

## AWS Services Used

* Amazon EC2
* Amazon EBS
* AWS Lambda
* Amazon EventBridge Scheduler
* AWS IAM
* Amazon CloudWatch Logs

---

## Runtime

* Python 3.12
* Boto3 SDK

---

## Architecture

```text
                  Amazon EventBridge Scheduler
                         (Weekly Schedule)
                                  |
                                  |
                                  ▼
                       AWS Lambda Function
                       (Python 3.12)
                                  |
              ┌───────────────────┴───────────────────┐
              |                                       |
              ▼                                       ▼
       Create EBS Snapshot                  Describe Existing Snapshots
              |                                       |
              ▼                                       ▼
       Add Snapshot Tag              Delete Snapshots Older Than 30 Days
       CreatedBy=Lambda-Backup
              |
              ▼
        CloudWatch Logs
```

---

# Prerequisites

* AWS Account
* AWS Region: `us-east-1` (recommended)
* EC2 instance with an attached EBS volume
* Lambda execution role with required permissions

---

# EBS Setup

1. Created/selected an EC2 instance using:

```
Instance Type: t3.micro
```

2. Identified the attached EBS volume.

Example:

```
Volume ID:
vol-xxxxxxxxxxxxxxxxx
```

The Lambda function uses this volume ID to create snapshots.

---

# IAM Permissions

The Lambda execution role follows the least privilege approach.

Required permissions:

```text
ec2:CreateSnapshot
ec2:DescribeSnapshots
ec2:DeleteSnapshot
ec2:CreateTags
```

CloudWatch logging permissions:

```text
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

The permissions are defined in:

```
IAM-Policy.json
```

---

# Solution Overview

The Lambda function performs the following operations:

## 1. Create EBS Snapshot

The function creates a snapshot using:

```python
ec2.create_snapshot()
```

The created snapshot is tagged:

```
CreatedBy = Lambda-Backup
```

---

## 2. Identify Existing Lambda Snapshots

The function searches snapshots owned by the current AWS account using:

```
OwnerIds=["self"]
```

and filters snapshots with:

```
CreatedBy=Lambda-Backup
```

---

## 3. Delete Old Snapshots

Snapshots are checked against the retention period:

```
Retention Period = 30 Days
```

Snapshots older than 30 days are deleted automatically.

---

## 4. Logging

The function prints:

* Created snapshot ID
* Deleted snapshot IDs

Example:

```
Created Snapshot: snap-0123456789abcdef

Deleted Snapshot: snap-0987654321abcdef
```

Logs are available in:

```
Amazon CloudWatch Logs
```

---

# EventBridge Scheduler Configuration

The Lambda function is scheduled using Amazon EventBridge Scheduler.

Schedule:

```
rate(7 days)
```

Target:

```
AWS Lambda
        |
        |
        ▼
ebs-snapshot-cleanup
```

The schedule triggers the Lambda function automatically every week.

---

# Testing

## Manual Lambda Test

A manual test event was created:

```json
{}
```

Expected response:

```json
{
    "statusCode": 200,
    "createdSnapshot": "snap-xxxxxxxxxxxxxxxx",
    "deletedSnapshots": []
}
```

---

## Verification Steps

1. Trigger Lambda manually.
2. Check CloudWatch Logs.
3. Navigate to:

```
EC2
→ Snapshots
```

4. Confirm:

   * New snapshot exists.
   * Snapshot contains tag:

```
CreatedBy = Lambda-Backup
```

---

# Screenshots

Store screenshots in:

```
Task2/screenshots/
```

Required screenshots:

| Screenshot           | Description                         |
| -------------------- | ----------------------------------- |
| ec2-instance.png     | EC2 instance configuration          |
| ebs-volume.png       | EBS volume ID                       |
| lambda-config.png    | Lambda Python 3.12 configuration    |
| iam-role.png         | IAM inline policy                   |
| eventbridge-rule.png | EventBridge Scheduler configuration |
| cloudwatch-logs.png  | Lambda execution logs               |
| snapshot-created.png | Created EBS snapshot                |
| snapshot-cleanup.png | Snapshot cleanup verification       |

---

# Production Discussion

AWS Data Lifecycle Manager (DLM) is the recommended solution for standard EBS snapshot automation because it provides native snapshot scheduling, retention management, and lifecycle policies without requiring custom code.

AWS Lambda is more suitable when additional customization is required, such as:

* Custom retention rules
* Cross-account snapshot copying
* Sending notifications after backup completion
* Integrating with other AWS services
* Applying business-specific backup conditions

---

# Cleanup

After testing:

* Delete EventBridge Scheduler.
* Delete Lambda function.
* Delete IAM role.
* Delete test EBS snapshots.
* Stop or terminate EC2 instances.
* Release unused resources.

This prevents unnecessary AWS charges.

---

# Repository Structure

```
Task2/
│
├── README.md
├── lambda_function_task2.py
├── IAM-Policy.json
├── architecture.png
│
└── screenshots/
    ├── ec2-instance.png
    ├── ebs-volume.png
    ├── lambda-config.png
    ├── iam-role.png
    ├── eventbridge-rule.png
    ├── cloudwatch-logs.png
    ├── snapshot-created.png
    └── snapshot-cleanup.png
```

---

## Author

Rashmi

## Assignment

AWS Lambda Assignments

Task2 - Automated EBS Snapshot Creation and Cleanup
