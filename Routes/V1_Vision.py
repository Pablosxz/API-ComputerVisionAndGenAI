import json
import boto3

# importing functions from the utils folder
from utils.createdDate import createdDate
from utils.verifyFaces import verifyFaces

def v1Vision(event, context):
    try:
        # Informations from the request
        request_body = json.loads(event.get('body'))
        bucket = request_body.get('bucket')
        imageName = request_body.get('imageName')

        # Initialize the boto3 session and client
        session = boto3.Session()
        client = session.client('rekognition')

        # Detecting faces in the image
        response_face = client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': imageName}},
            Attributes=['ALL']
        )

        # Logging the response on CloudWatch
        log = json.dumps(response_face)
        print(log)

        # URL to the image
        url = f'https://{bucket}.s3.amazonaws.com/{imageName}'

        # Get the created date of the image
        created_image = createdDate(bucket, imageName)

        # Initialize the body of the response
        body = {
            "url_to_image": url,
            "created_image": created_image,
            "faces": []
        }

        # Verifying faces in the image
        body = verifyFaces(response_face, body)

        response = {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        response = {"statusCode": 500, "body": json.dumps({"message": str(e)})}

    return response