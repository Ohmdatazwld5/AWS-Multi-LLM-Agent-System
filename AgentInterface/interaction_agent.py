import os
import json
import boto3

# Initialize the SQS client and get the queue URL from environment variables
sqs = boto3.client("sqs")
QUEUE_URL = os.environ["SQS_QUEUE_URL"]

def lambda_handler(event, context):
    """
    AWS Lambda handler for ingesting feedback via API Gateway.
    Validates required fields and enqueues the feedback for asynchronous processing.
    """
    try:
        # Parse the API Gateway body (event["body"] is a JSON string)
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        # Define required fields
        required_fields = {"feedback_id", "customer_name", "feedback_text", "timestamp"}
        missing = required_fields - set(body.keys())
        if missing:
            return {
                "statusCode": 400,
                "body": f"Missing fields: {', '.join(missing)}"
            }

        # TODO: Add further guardrails or input validation here, such as checking string lengths or forbidden words

        # Send the feedback to SQS for downstream processing
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )

        return {
            "statusCode": 200,
            "body": "Submitted for processing."
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
