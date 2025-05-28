import os
import json
import boto3
import requests
from decimal import Decimal

from tools import sentiment_analysis, topic_categorization, keyword_extraction, summarization

# Initialize DynamoDB table resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DDB_TABLE'])

# Groq API configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = os.environ.get(
    "GROQ_API_URL",
    "https://api.groq.com/v1/chat/completions"
)
GROQ_MODEL = os.environ.get("GROQ_MODEL", "mixtral-8x7b-32768")

# List of all possible analysis tools
DEFAULT_TOOLS = [
    'sentiment_analysis',
    'topic_categorization',
    'keyword_extraction',
    'summarization'
]

def call_groq_llm(instructions):
    """
    Uses Groq LLM to select which analysis tools to use, based on user instructions.
    Returns a list of tool names.
    """
    prompt = (
        "You are an agent that selects which of the following tools to run "
        f"based on the user's instructions. The available tools are: {', '.join(DEFAULT_TOOLS)}. "
        f"The instructions are: '{instructions}'. "
        "Reply with a comma-separated list of tool names to execute."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    selected = [tool.strip() for tool in content.split(",") if tool.strip() in DEFAULT_TOOLS]
    return selected if selected else DEFAULT_TOOLS

def determine_tools(instructions):
    """
    Determines which analysis tools to run based on user instructions.
    If instructions are provided, uses the LLM; otherwise, defaults to all tools.
    """
    if instructions and str(instructions).strip():
        try:
            return call_groq_llm(instructions)
        except Exception as e:
            print(f"Groq API call failed, defaulting to all tools: {e}")
            return DEFAULT_TOOLS
    else:
        return DEFAULT_TOOLS

def convert_floats_to_decimal(obj):
    """
    Recursively converts float values to Decimal for DynamoDB compatibility.
    """
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats_to_decimal(i) for i in obj]
    else:
        return obj

def lambda_handler(event, context):
    """
    AWS Lambda entrypoint.
    Processes each record in the event, runs selected analyses, and stores results in DynamoDB.
    """
    for record in event['Records']:
        try:
            message = json.loads(record['body'])
            feedback_id = message['feedback_id']
            print(f"Processing feedback_id: {feedback_id}")

            # Check if already processed
            existing = table.get_item(Key={'feedback_id': feedback_id})
            if 'Item' in existing:
                print(f"Feedback {feedback_id} already exists in DynamoDB, skipping.")
                continue

            # Select tools
            tools = determine_tools(message.get('instructions'))
            print(f"Tools selected for {feedback_id}: {tools}")
            results = {}
            text = message['feedback_text']

            # Run analyses as needed
            if 'sentiment_analysis' in tools:
                results['sentiment'] = sentiment_analysis.analyze(text)
                print(f"Sentiment result for {feedback_id}: {results['sentiment']}")

            if 'topic_categorization' in tools:
                results['topics'] = topic_categorization.categorize(text)
                print(f"Topic categorization result for {feedback_id}: {results['topics']}")

            if 'keyword_extraction' in tools:
                results['keywords'] = keyword_extraction.extract(text)
                print(f"Keyword extraction result for {feedback_id}: {results['keywords']}")

            if 'summarization' in tools:
                results['summary'] = summarization.summarize(text)
                print(f"Summarization result for {feedback_id}: {results['summary']}")

            print(f"Full results for {feedback_id}: {results}")

            # Prepare results for DynamoDB
            results_decimal = convert_floats_to_decimal(results)
            message_decimal = convert_floats_to_decimal(message)

            table.put_item(Item={
                'feedback_id': feedback_id,
                'results': results_decimal,
                'original_feedback': message_decimal
            })
            print(f"Results for {feedback_id} stored successfully in DynamoDB.")

        except Exception as e:
            print(f"Error processing {feedback_id}: {e}")
            raise e

    return {'statusCode': 200}
