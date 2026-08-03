import json
import os

from agent.bedrock_client import get_bedrock_client


EMBEDDING_DIMENSIONS = 1024


def generate_embedding(text):
    model_id = os.getenv("EMBEDDING_MODEL", "amazon.titan-embed-text-v2:0")
    client = get_bedrock_client()

    response = client.invoke_model(
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
        body=json.dumps(
            {
                "inputText": text,
                "dimensions": EMBEDDING_DIMENSIONS,
                "normalize": True,
                "embeddingTypes": ["float"],
            }
        ),
    )

    response_body = json.loads(response["body"].read())
    return response_body["embedding"]


def vector_to_sql(vector):
    return "[" + ",".join(str(value) for value in vector) + "]"
