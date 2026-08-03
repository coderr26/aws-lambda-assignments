# AWS Lambda Assignments

## Overview

This repository contains AWS Lambda automation assignments implemented using AWS serverless services and Python 3.12.

The assignments demonstrate:

* AWS Lambda automation
* Amazon EventBridge event-driven workflows
* Least privilege IAM policies
* AWS SDK (Boto3) integrations
* Amazon CloudWatch logging
* AWS resource automation and monitoring

---

## Completed Assignments

| Task  | Description                                                                                              |
| ----- | -------------------------------------------------------------------------------------------------------- |
| Task1 | Automated S3 Bucket Cleanup - Deletes stale S3 objects older than configured retention period            |
| Task2 | Automated EBS Snapshot Creation and Cleanup - Creates EBS backups and removes expired snapshots          |
| Task3 | Auto-Tagging EC2 Instances on Launch - Automatically tags EC2 instances using EventBridge and Lambda     |
| Task4 | Daily AWS Cost Alert Using Cost Explorer API and SNS - Sends cost alerts based on AWS spending threshold |

---

## AWS Services Used

* AWS Lambda (Python 3.12)
* Amazon S3
* Amazon EC2
* Amazon EBS
* Amazon EventBridge
* AWS IAM
* AWS Cost Explorer API
* Amazon SNS
* Amazon CloudWatch Logs

---

## Repository Structure

```
aws-lambda-assignments

├── README.md

├── Task1
│   ├── README.md
│   └── Lambda code

├── Task2
│   ├── README.md
│   └── Lambda code

├── Task3
│   ├── README.md
│   └── Lambda code

└── Task4
    ├── README.md
    └── Lambda code
```

Each task folder contains:

* Assignment documentation
* Lambda implementation
* IAM permission details
* AWS configuration steps
* Testing details
* Screenshots (where applicable)

---

## Assignment Repository

GitHub:

https://github.com/coderr26/aws-lambda-assignments

---

## Notes

All assignments follow AWS best practices:

* Python 3.12 Lambda runtime
* Least privilege IAM permissions
* EventBridge for scheduling and event automation
* CloudWatch logging for visibility
* AWS resource cleanup after testing to minimize cost

---

## Author

AWS Lambda Automation Assignment Submission
touch is /usr/bin/touch
