import json
import boto3

from utils.labelFilter import labelFilter

def v2_vision(event, context):
    try:
        # Informações da solicitação
        request_body = json.loads(event.get('body'))
        bucket = request_body.get('bucket')
        imageName = request_body.get('imageName')

        # Inicializando o cliente do Rekognition
        session = boto3.Session()
        client = session.client('rekognition')

        # Detectando animais na imagem
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

        # Pegando a 'confidence' e 'name' das labels
        labels = [
            {
                'Confidence': label['Confidence'],
                'Name': label['Name']
            }
            for label in response_animal['Labels']
        ]

        # Filtering Labels
        labels = labelFilter(labels)

        # Verificar se há PET na imagem
        if len(labels) == 0: 
            raise Exception("Não foi possível identificar pets na imagem.")

        # Montando a URL da imagem
        url = f'https://{bucket}.s3.amazonaws.com/{imageName}'

        # Pegando a data de criação da imagem
        s3 = boto3.client('s3')
        dados = s3.head_object(Bucket=bucket, Key=imageName)
        created_image = dados['LastModified'].strftime("%d-%m-%Y %H:%M:%S")

        # Gerando dados com AWS Bedwrock
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name="us-east-1"
        )

        # Prompt
        label_names = [label["Name"] for label in labels]
        prompt = f"""
Labels: {label_names}

Tarefa: Com base na lista de labels do animal informado anteriormente, detecte o parâmetro relacionado a raça deste e dê dicas sobre o nível de energia e necessidades de exercícios,
temperamento e comportamento, cuidados e necessidades, problemas de saúde comuns desse animal. Se refira ao pet por sua
raça e não por sua espécie. Tente usar as labels informadas.

Exemplo de saída: Dicas sobre a raça Labrador: 
Nível de Energia e Necessidades de Exercícios: Labradores são de médio nível de energia, necessitando de 40 minutos de exercício por dia. 
Temperamento e Comportamento: Inteligentes, enérgicos, dóceis, e com forte desejo de trabalhar com pessoas. 
Cuidados e Necessidades: Pelos curtos que precisam de poucos cuidados, mas devem ser penteados uma vez por semana para remover fios mortos e soltos. A alimentação deve ser adequada, ajustando a quantidade conforme o peso do cão. 
Problemas de Saúde Comuns: Displasia do cotovelo e coxofemoral, atrofia progressiva da retina (APR) e catarata hereditária. 
        """

        # Corpo da requisição ao modelo
        bedrock_request_body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "stopSequences": [],
                "temperature": 0,
                "topP": 0.9
            }
        })

        # Chamada ao modelo
        model_response = bedrock_runtime.invoke_model(
            body=bedrock_request_body,
            modelId="amazon.titan-text-express-v1",
            accept="application/json",
            contentType="application/json",
        )

        # Resposta do modelo
        response_content = json.loads(model_response.get('body').read())
        generated_text = response_content.get('results')[0].get('outputText')
        generated_text = generated_text.replace("\n", " ")

        # Montando o corpo da resposta
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