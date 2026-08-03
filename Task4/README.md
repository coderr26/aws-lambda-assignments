# AWS Daily Cost Alert using Lambda, Cost Explorer API, EventBridge & SNS

## Project Overview

This project automatically monitors AWS month-to-date spending using the AWS Cost Explorer API. If the total AWS cost exceeds a configured threshold, an email notification is sent through Amazon SNS.

The solution is completely serverless and runs automatically every day using Amazon EventBridge Scheduler.

---

## Architecture

```
               EventBridge Scheduler
                    (Daily)
                       │
                       ▼
               AWS Lambda Function
                       │
        Calls Cost Explorer API
                       │
      Retrieves Month-to-Date Cost
                       │
       Compare with Threshold
                       │
          ┌────────────┴────────────┐
          │                         │
     Cost < Threshold        Cost > Threshold
          │                         │
          │                         ▼
          │                  Amazon SNS Topic
          │                         │
          └────────────────────────►Email Alert
```

---

## AWS Services Used

- AWS Lambda
- Amazon EventBridge Scheduler
- Amazon SNS
- AWS Cost Explorer API
- AWS IAM
- Amazon CloudWatch Logs

---

## Project Workflow

1. EventBridge Scheduler invokes the Lambda function once every day.
2. Lambda calls the AWS Cost Explorer API.
3. Retrieves Month-to-Date Unblended Cost.
4. Compares the current cost against the configured threshold.
5. If the threshold is exceeded:
   - Publishes a message to an SNS topic.
   - SNS sends an email notification.
6. Lambda execution logs are stored in CloudWatch Logs.

---

## Prerequisites

- AWS Account
- Cost Explorer Enabled
- AWS Lambda
- Amazon SNS
- Amazon EventBridge Scheduler
- IAM Permissions
- Verified Email Subscription

---

## Project Structure

```
aws-daily-cost-alert/
│
├── lambda_function.py
├── requirements.txt
├── README.md
├── iam-policy.json
├── screenshots/
│   ├── lambda-function.png
│   ├── sns-topic.png
│   ├── eventbridge-schedule.png
│   ├── cloudwatch-logs.png
│   └── email-alert.png
```

---

# Step 1 : Create SNS Topic

1. Open Amazon SNS.
2. Create a **Standard Topic**.
3. Name:

```
aws-cost-alert
```

4. Create the topic.

---

# Step 2 : Subscribe Email

Create Email Subscription.

Protocol

```
Email
```

Endpoint

```
your-email@example.com
```

Confirm the subscription from your email inbox.

---

# Step 3 : Create IAM Role for Lambda

Attach the following permissions.

## Cost Explorer

```
ce:GetCostAndUsage
```

## SNS

```
sns:Publish
```

Sample IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Step 4 : Create Lambda Function

Runtime

```
Python 3.13
```

Function Name

```
daily-cost-alert
```

Deploy the following code.

---

## Lambda Function

```python
import boto3
from datetime import date

ce = boto3.client("ce")
sns = boto3.client("sns")

SNS_TOPIC = "YOUR_SNS_TOPIC_ARN"

THRESHOLD = 50

def lambda_handler(event, context):

    today = date.today()

    start = today.replace(day=1).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start,
            "End": end
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = float(
        response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    )

    print(f"Current Cost: ${amount}")

    if amount > THRESHOLD:

        sns.publish(
            TopicArn=SNS_TOPIC,
            Subject="AWS Cost Alert",
            Message=f"Current AWS cost is ${amount}"
        )

        print("Alert Sent")

    return {
        "statusCode": 200
    }
```

---

# Step 5 : Test Lambda

Lower the threshold for testing.

```python
THRESHOLD = 0.01
```

Click

```
Deploy
```

Click

```
Test
```

Expected Output

```
Status Code: 200

Current Cost: $0.xx

Alert Sent
```

Check your email.

---

# Step 6 : Create EventBridge Scheduler

Navigate to

```
Amazon EventBridge

↓

Scheduler

↓

Create Schedule
```

Configuration

Schedule Name

```
daily-cost-alert
```

Pattern

```
Recurring
```

Cron

```
cron(0 9 * * ? *)
```

Runs every day at **9:00 UTC**.

Target

```
AWS Lambda
```

Lambda Function

```
daily-cost-alert
```

Create a new execution role.

Review and Create.

---

# Step 7 : Verify

## EventBridge

```
Status

Enabled
```

Target

```
daily-cost-alert
```

---

## Lambda Trigger

```
Configuration

↓

Triggers
```

Should display

```
EventBridge Scheduler
```

---

## CloudWatch Logs

Navigate

```
CloudWatch

↓

Log Groups

↓

/aws/lambda/daily-cost-alert
```

Example

```
Current Cost: $0.32

Alert Sent
```

---

## Expected Email

Subject

```
AWS Cost Alert
```

Message

```
Current AWS cost is $0.32

Threshold exceeded.
```

---

# GitHub Repository

```
git init

git add .

git commit -m "AWS Daily Cost Alert using Lambda"

git branch -M main

git remote add origin https://github.com/<username>/aws-daily-cost-alert.git

git push -u origin main
```

---

# Advantages

- Fully Serverless
- No EC2 Required
- Automated Daily Monitoring
- Email Notifications
- Easy to Extend
- Low Cost
- Scalable

---

# Future Enhancements

- Slack Notifications
- Microsoft Teams Integration
- Per-Service Cost Alerts
- Cost Anomaly Detection
- Daily Cost Reports
- Store Cost History in DynamoDB
- Visualize Costs in Amazon QuickSight

---

# Interview Questions

### Why use Cost Explorer API instead of CloudWatch Billing Metrics?

CloudWatch Billing metrics are a legacy feature and only available in the us-east-1 region after manual activation. The Cost Explorer API is the modern and recommended approach, providing richer cost data and greater flexibility.

---

### Why EventBridge Scheduler?

EventBridge Scheduler allows fully managed, serverless scheduling of Lambda functions without requiring any infrastructure or cron servers.

---

### Why SNS?

SNS provides a simple, scalable notification service that can send alerts via Email, SMS, HTTP endpoints, Lambda, and many other integrations.

---

### When would you use AWS Budgets instead?

AWS Budgets is suitable for simple budget alerts with minimal configuration. A custom Lambda solution is preferred when advanced logic is required, such as:
- Per-service cost monitoring
- Slack or Microsoft Teams notifications
- Cost anomaly detection
- Custom business rules
- Integration with external systems

---

## Author

**Rashmi R**

AWS | DevOps | Site Reliability Engineering (SRE)
