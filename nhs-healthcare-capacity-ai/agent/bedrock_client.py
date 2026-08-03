import os

import boto3
from dotenv import load_dotenv


load_dotenv()


def get_bedrock_client():
    region_name = os.getenv("AWS_REGION", "us-east-1")

    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name,
    )


def generate_text(prompt):
    model_id = os.getenv("BEDROCK_TEXT_MODEL", "amazon.nova-pro-v1:0")
    client = get_bedrock_client()

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": 500,
            "temperature": 0.2,
        },
    )

    return response["output"]["message"]["content"][0]["text"]