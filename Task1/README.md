# Task1 - Automated S3 Bucket Cleanup (Objects Older Than 30 Days)

## Objective

Automate the deletion of stale objects from an Amazon S3 bucket using AWS Lambda. The function identifies objects older than 30 days and removes them automatically while logging the affected object names to Amazon CloudWatch Logs.

---

## AWS Services Used

* AWS Lambda (Python 3.12)
* Amazon S3
* AWS Identity and Access Management (IAM)
* Amazon CloudWatch Logs

---

## Architecture

```
Amazon S3 Bucket
       │
       ▼
AWS Lambda (Python 3.12)
       │
       ├── List Objects (Paginator)
       ├── Compare LastModified with Current UTC Time
       ├── Delete Objects Older Than 30 Days
       └── Log Deleted Object Names to CloudWatch
```

---

## Prerequisites

* AWS Account
* AWS Region: **us-east-1** (recommended)
* Python Runtime: **Python 3.12**
* An S3 bucket containing test files

---

## IAM Permissions

The Lambda execution role follows the **least-privilege principle** and includes only the required permissions:

* `s3:ListBucket`
* `s3:DeleteObject`
* `logs:CreateLogGroup`
* `logs:CreateLogStream`
* `logs:PutLogEvents`

---

## Solution Overview

The Lambda function performs the following steps:

1. Connects to Amazon S3 using Boto3.
2. Uses an S3 paginator to list all objects in the specified bucket.
3. Retrieves each object's `LastModified` timestamp.
4. Compares it with the current UTC time.
5. Deletes objects older than **30 days**.
6. Prints the names of deleted objects to CloudWatch Logs.
7. Returns a list of deleted objects in the Lambda response.

---

## Testing

Because creating 30-day-old objects for testing is impractical, the retention threshold was temporarily reduced from **30 days** to **5 minutes**.

### Test Steps

1. Create an S3 bucket.
2. Upload several files.
3. Wait at least five minutes.
4. Invoke the Lambda function manually.
5. Verify that only the older files are deleted.
6. Restore the final code to use a **30-day** retention period before submission.

---

## Sample Output

### Lambda Response

```json
{
  "statusCode": 200,
  "deletedObjects": [
    "test1.rtf",
    "test2.rtf",
    "test3.rtf"
  ]
}
```

### CloudWatch Logs

```
Deleted object: test1.rtf
Deleted object: test2.rtf
Deleted object: test3.rtf
```

---

## Screenshots

Include the following screenshots in the `screenshots/` folder:

* `s3-bucket.png` – S3 bucket with uploaded files
* `lambda-config.png` – Lambda function configuration (Python 3.12)
* `iam-role.png` – IAM role and inline policy
* `cloudwatch-logs.png` – CloudWatch execution logs
* `test-result.png` – S3 bucket after cleanup

---

## Production Discussion

Amazon S3 Lifecycle Rules are the preferred solution for simple age-based object deletion because they are fully managed, require no custom code, and have minimal operational overhead.

AWS Lambda is a better choice when deletion depends on custom business logic, object naming patterns, metadata, or when additional actions such as sending notifications or invoking other AWS services are required.

---

## Repository Contents

```
Task1/
│
├── README.md
├── lambda_function_task1.py
├── IAM-Policy.json
├── architecture.png
└── screenshots/
    ├── s3-bucket.png
    ├── lambda-config.png
    ├── iam-role.png
    ├── cloudwatch-logs.png
    └── test-result.png
```

---

## Cleanup

After testing:

* Delete all objects from the S3 bucket.
* Delete the S3 bucket.
* Delete the Lambda function.
* Delete the IAM role if it is no longer needed.
* Remove the CloudWatch log group (optional).
* Verify that no unused AWS resources remain.

---

## Author

**Name:** Rashmi
**Repository:** AWS Lambda Assignments
**Task:** Task1 – Automated S3 Bucket Cleanup
touch is /usr/bin/touch
