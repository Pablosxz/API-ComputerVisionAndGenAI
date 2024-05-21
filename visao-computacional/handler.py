import json
import boto3

from Routes.V1_Vision import v1_vision
from Routes.V2_Vision import v2_vision

def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_description(event, context):
    body = {
        "message": "VISION api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v2_description(event, context):
    body = {
        "message": "VISION api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_vision(event, context):
    return v1_vision(event, context)


def v2_vision(event, context):
    return v2_vision(event, context)
