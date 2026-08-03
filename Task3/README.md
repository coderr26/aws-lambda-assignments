# Task3 - Auto-Tagging EC2 Instances on Launch

## Objective

Automatically tag newly launched EC2 instances for resource tracking, ownership, and cost allocation.

When an EC2 instance changes its state to **running**, Amazon EventBridge triggers an AWS Lambda function. The Lambda function extracts the instance ID from the event and automatically adds custom tags to the instance.

Example tags:

```
LaunchDate = 2026-08-03
Environment = Development
Owner = Lambda-Automation
```

---

# AWS Services Used

| AWS Service            | Purpose                             |
| ---------------------- | ----------------------------------- |
| Amazon EC2             | Launch and manage instances         |
| AWS Lambda             | Execute tagging automation          |
| Amazon EventBridge     | Detect EC2 state change events      |
| AWS IAM                | Provide least-privilege permissions |
| Amazon CloudWatch Logs | Monitor Lambda execution            |

---

# Architecture

```
EC2 Instance Launch
        |
        |
        v
EC2 State Change Event
(state = running)
        |
        |
        v
Amazon EventBridge Rule
(EC2-Auto-Tag-Rule)
        |
        |
        v
AWS Lambda Function
(ec2-auto-tag)
        |
        |
        v
EC2 CreateTags API
        |
        |
        v
EC2 Instance Tags Added
```

---

# Step 1: IAM Role Setup

## IAM Role

Role Name:

```
lambda-ec2-auto-tag-role
```

Trusted Service:

```
AWS Lambda
```

---

## Inline IAM Policy

The Lambda execution role uses a least-privilege inline policy.

Required permissions:

* `ec2:CreateTags`
* `ec2:DescribeInstances`
* CloudWatch Logs permissions

IAM Policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2TagPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchLogs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

---

# Step 2: Lambda Function

## Lambda Configuration

| Setting       | Value                    |
| ------------- | ------------------------ |
| Function Name | ec2-auto-tag             |
| Runtime       | Python 3.12              |
| Role          | lambda-ec2-auto-tag-role |

---

## Lambda Logic

The function performs the following actions:

1. Receives EC2 state change event from EventBridge.
2. Extracts instance ID from:

```
event["detail"]["instance-id"]
```

3. Creates tags:

   * LaunchDate
   * Environment
   * Owner

4. Uses EC2 `CreateTags` API.

5. Prints confirmation message to CloudWatch Logs.

---

## Lambda Function File

```
lambda_function_task3.py
```

The function uses:

```python
import boto3
from datetime import datetime, timezone
```

and creates EC2 tags using:

```python
ec2.create_tags()
```

---

# Step 3: EventBridge Rule

## Rule Configuration

Rule Name:

```
EC2-Auto-Tag-Rule
```

Description:

```
Automatically tag EC2 instances when they enter running state
```

Event Bus:

```
default
```

Status:

```
Enabled
```

---

## Event Pattern

The rule matches:

* Event source: `aws.ec2`
* Event type: EC2 Instance State-change Notification
* Instance state: running

Event pattern:

```json
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "running"
    ]
  }
}
```

---

# Step 4: Configure EventBridge Target

Target Type:

```
AWS Lambda
```

Target Function:

```
ec2-auto-tag
```

EventBridge permission:

```
Create a new role for this specific resource
```

AWS creates an invocation role:

```
Amazon_EventBridge_Invoke_Lambda_xxxxx
```

Purpose:

```
EventBridge → Invoke Lambda
```

---

# Step 5: Testing

## Launch EC2 Instance

Create a new EC2 instance.

Configuration:

| Setting       | Value             |
| ------------- | ----------------- |
| AMI           | Amazon Linux 2023 |
| Instance Type | t3.micro          |

Example instance name:

```
task3-test-instance
```

---

## Event Flow

```
EC2 Instance
     |
     |
Instance state changes:
pending → running
     |
     |
EventBridge Rule
     |
     |
Lambda Function
     |
     |
CreateTags API
```

---

# Step 6: Verify Tags

Navigate:

```
EC2 Console
→ Instances
→ Select Instance
→ Tags
```

Expected tags:

| Key         | Value               |
| ----------- | ------------------- |
| Name        | task3-test-instance |
| LaunchDate  | 2026-08-03          |
| Environment | Development         |
| Owner       | Lambda-Automation   |

---

# Step 7: CloudWatch Logs Verification

Navigate:

```
CloudWatch
→ Log Groups
→ /aws/lambda/ec2-auto-tag
```

Expected log output:

```
Received Event:

instance-id=i-xxxxxxxxxxxx

Successfully tagged EC2 instance i-xxxxxxxxxxxx
```

---

# Bonus: Dynamic Owner Tag Using CloudTrail

Instead of assigning a fixed owner:

```
Owner = Lambda-Automation
```

CloudTrail can be used to identify the IAM user who launched the instance.

Flow:

```
IAM User
    |
    |
RunInstances API
    |
    |
CloudTrail Event
    |
    |
EventBridge
    |
    |
Lambda
    |
    |
EC2 CreateTags
```

The Lambda function can extract:

```
userIdentity.userName
```

and assign:

```
Owner = <IAM Username>
```

Benefits:

* Automatic ownership tracking
* Better cost allocation
* Improved auditing
* Resource governance

---

# Cleanup

After testing, remove resources to avoid charges.

## EC2

Terminate test instances:

```
EC2 Console
→ Instances
→ Terminate
```

## EventBridge

Delete:

```
EC2-Auto-Tag-Rule
```

## Lambda

Delete:

```
ec2-auto-tag
```

## IAM

Delete:

```
lambda-ec2-auto-tag-role
```

---

# Screenshots

Store screenshots inside:

```
Task3/screenshots/
```

Recommended screenshots:

```
iam-role-policy.png
lambda-function.png
eventbridge-rule.png
ec2-instance-running.png
ec2-instance-tags.png
cloudwatch-logs.png
```

---

# Folder Structure

```
Task3
│
├── README.md
├── lambda_function_task3.py
├── IAM-Policy.json
├── event-pattern.json
│
└── screenshots
    ├── iam-role-policy.png
    ├── lambda-function.png
    ├── eventbridge-rule.png
    ├── ec2-instance-tags.png
    └── cloudwatch-logs.png
```

---

# Completion Status

✅ Lambda Function Created
✅ IAM Least Privilege Policy Configured
✅ EventBridge Rule Created
✅ EC2 Auto Tagging Tested
✅ CloudWatch Logs Verified
