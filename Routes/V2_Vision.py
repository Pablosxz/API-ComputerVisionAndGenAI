import json
import boto3

# importing functions from the utils folder
from utils.labelFilter import labelFilter
from utils.createdDate import createdDate

def v2Vision(event, context):
    try:
        # Request Info
        request_body = json.loads(event.get('body'))
        bucket = request_body.get('bucket')
        imageName = request_body.get('imageName')

        # Inicializing session and AWS Rekognition
        session = boto3.Session()
        client = session.client('rekognition')

        # Detecting animals in the image
        response_animal = client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': imageName}},
            Features = ["GENERAL_LABELS"],
            Settings = {
                "GeneralLabels" :
                    {
                        "LabelCategoryInclusionFilters" : ["Animals and Pets"]
                    }
            },
        )

        # Getting 'confidence' and 'name' from the labels
        labels = [
            {
                'Confidence': label['Confidence'],
                'Name': label['Name']
            }
            for label in response_animal['Labels']
        ]

        # Filtering Labels
        labels = labelFilter(labels)

        # Verify if there is any label
        if len(labels) == 0: 
            raise Exception("Unable to identify pets in the image.")

        # Image URL
        url = f'https://{bucket}.s3.amazonaws.com/{imageName}'

        # Getting the image creation date
        created_image = createdDate(bucket, imageName)

        # Bedrock
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name="us-east-1"
        )

        # Prompt
        label_names = [label["Name"] for label in labels]
        prompt = f"""
Labels: {label_names}

Task: Based on the list of labels of the animal previously informed, detect the parameter related to its breed and give tips on its energy level and exercise needs, temperament and behavior, care and needs, and common health problems of this animal. Refer to the pet by its breed and not by its species. Try to use the informed labels.

Example output: Tips about the Labrador breed:
Energy Level and Exercise Needs: Labradors have a medium energy level, requiring 40 minutes of exercise per day.
Temperament and Behavior: Intelligent, energetic, docile, and with a strong desire to work with people.
Care and Needs: Short hair that needs little care, but should be brushed once a week to remove dead and loose hair. The diet should be adequate, adjusting the amount according to the dog's weight.
Common Health Problems: Elbow and hip dysplasia, progressive retinal atrophy (PRA), and hereditary cataracts.
        """

        # Body of the request
        bedrock_request_body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "stopSequences": [],
                "temperature": 0,
                "topP": 0.9
            }
        })

        # Calling the model
        model_response = bedrock_runtime.invoke_model(
            body=bedrock_request_body,
            modelId="amazon.titan-text-express-v1",
            accept="application/json",
            contentType="application/json",
        )

        # Answer from the model
        response_content = json.loads(model_response.get('body').read())
        generated_text = response_content.get('results')[0].get('outputText')
        generated_text = generated_text.replace("\n", " ")

        # Response body
        body = {
            "url_to_image": url,
            "created_image": created_image,
            "labels": labels[:4],
            "Dicas": generated_text[1:],
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

    return response