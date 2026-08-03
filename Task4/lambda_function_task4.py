import os
import boto3
from datetime import date

# AWS Clients
ce = boto3.client("ce")
sns = boto3.client("sns")

# Environment Variables
SNS_TOPIC = os.environ["SNS_TOPIC_ARN"]
THRESHOLD = float(os.environ.get("THRESHOLD", "50"))


def lambda_handler(event, context):
    # Current month start and today's date
    start = date.today().replace(day=1).strftime("%Y-%m-%d")
    end = date.today().strftime("%Y-%m-%d")

    # Get Month-to-Date AWS Cost
    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start,
            "End": end
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    current_cost = float(
        response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    )

    print(f"Current AWS Month-to-Date Cost: ${current_cost:.2f}")

    # Send SNS Alert if threshold exceeded
    if current_cost > THRESHOLD:
        message = f"""
AWS Daily Cost Alert

Current Month-to-Date Cost : ${current_cost:.2f}
Threshold                 : ${THRESHOLD:.2f}

Your AWS spending has exceeded the configured threshold.
"""

        sns.publish(
            TopicArn=SNS_TOPIC,
            Subject="AWS Cost Alert",
            Message=message
        )

        print("Alert sent successfully.")

    else:
        print("Cost is within threshold.")

    return {
        "statusCode": 200,
        "body": {
            "current_cost": current_cost,
            "threshold": THRESHOLD
        }
    }