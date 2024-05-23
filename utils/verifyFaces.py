def verifyFaces(response_face, body):
    # verify if there is no face detected
    if not response_face['FaceDetails']:
        # Add a face with None values
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
        # Loop through the faces detected
        for faceDetail in response_face['FaceDetails']:

            # Get the most confident emotion
            emotion = sorted(
                faceDetail['Emotions'], key=lambda x: x['Confidence'], reverse=True)[0]

            # Add the face to the body
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
    
    return body