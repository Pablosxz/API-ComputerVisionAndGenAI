import json
import boto3

from utils.createdDate import createdDate

def v1_vision(event, context):
    try:
        # Informações da solicitação
        request_body = json.loads(event.get('body'))
        bucket = request_body.get('bucket')
        imageName = request_body.get('imageName')

        # Inicializando o cliente do Rekognition
        session = boto3.Session()
        client = session.client('rekognition')

        # Detectando faces na imagem
        response_face = client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': imageName}},
            Attributes=['ALL']
        )

        # Logando a resposta do Rekognition
        log = json.dumps(response_face)
        print(log)

        # Montando a URL da imagem
        url = f'https://{bucket}.s3.amazonaws.com/{imageName}'

        # Get the created date of the image
        created_image = createdDate(bucket, imageName)

        # Inicializando o corpo da resposta
        body = {
            "url_to_image": url,
            "created_image": created_image,
            "faces": []
        }

        # Verificando se não foi detectada nenhuma face
        if not response_face['FaceDetails']:
            # Adiciona a face NULA no corpo da resposta
            body["faces"].append({
                "position": {
                    "top": None,
                    "left": None,
                    "width": None,
                    "height": None
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None
            })
        else:
            # Para cada face detectada
            for faceDetail in response_face['FaceDetails']:

                # pega a emoção com maior confiança, que é a primeira da lista ordenada
                emotion = sorted(
                    faceDetail['Emotions'], key=lambda x: x['Confidence'], reverse=True)[0]

                # Adiciona a face no corpo da resposta
                body["faces"].append({
                    "position": {
                        "top": faceDetail['BoundingBox']['Top'],
                        "left": faceDetail['BoundingBox']['Left'],
                        "width": faceDetail['BoundingBox']['Width'],
                        "height": faceDetail['BoundingBox']['Height']
                    },
                    "classified_emotion": emotion['Type'],
                    "classified_emotion_confidence": emotion['Confidence']
                })

        response = {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        response = {"statusCode": 500, "body": json.dumps({"message": str(e)})}

    return response