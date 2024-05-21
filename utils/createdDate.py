import boto3

def createdDate(bucket, imageName):
    s3 = boto3.client('s3')
    dados = s3.head_object(Bucket=bucket, Key=imageName)
    created_image = dados['LastModified'].strftime("%d-%m-%Y %H:%M:%S")

    return created_image