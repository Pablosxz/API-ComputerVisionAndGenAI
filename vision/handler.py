import json
import boto3

# importing functions from the Routes folder
from Routes.health import health_function
from Routes.V1_Description import v1Description
from Routes.V2_Description import v2Description
from Routes.V1_Vision import v1Vision
from Routes.V2_Vision import v2Vision

# Routes
def health(event, context):
    return health_function(event, context)


def v1_description(event, context):
    return v1Description(event, context)


def v2_description(event, context):
    return v2Description(event, context)


def v1_vision(event, context):
    return v1Vision(event, context)


def v2_vision(event, context):
    return v2Vision(event, context)