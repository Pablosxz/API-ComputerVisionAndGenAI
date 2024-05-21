#  Detector de Emoções e Gerador de Dicas para Tutores de Pets

Avaliação da oitava sprint do programa de bolsas Compass UOL para formação em machine learning para AWS.

***

## 📃 Índice

- [Escopo do Projeto](#-escopo-do-projeto)
- [Ferramentas e tecnologias utilizadas](#-ferramentas-e-tecnologias-utilizadas)
- [Rotas da Aplicação](#-rotas-da-aplicação)
- [Como utilizar o sistema](#-como-utilizar-o-sistema)
- [Desenvolvimento](#-desenvolvimento)
- [Organização das Pastas](#-organização-das-pastas)
- [Dificuldades Conhecidas](#-Dificuldades-Conhecidas)
- [Desenvolvedores](#-desenvolvedores)

***

## 🔭 Escopo do Projeto

A API foi desenvolvida para visando realizar duas funcionalidades distintas:

- Detectar as emoções nos rostos presentes nas imagens enviadas como parâmetros.
- Detectar a raça de animais presentes nas fotos enviadas, além de gerar dicas buscando facilitar a criação de seus pets, sejam elas dicas de saúde ou de comportamentos que podem ser apresentados pelo seu bichinho.

***

## 🛠️ Ferramentas e tecnologias utilizadas

<div style="display: inline_block">
  <table border="1">
    <tr>
        <th>Tecnologia</th>
        <th>Versão</th>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="AWS CLI" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/AWS/svg/Developer-Tools/Command-Line-Interface.svg"></a>AWS CLI</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Boto 3" height="20" width="20" style="margin-right: 10px" src="https://boto3typed.gallerycdn.vsassets.io/extensions/boto3typed/boto3-ide/0.5.4/1680224848596/Microsoft.VisualStudio.Services.Icons.Default"></a>Boto 3</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Serverless" height="20" width="20" style="margin-right: 10px" src="https://static-00.iconduck.com/assets.00/serverless-icon-512x407-neft7ola.png"></a>Serverless</td>
        <td>V. 3.38</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Rekognition" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/AWS/svg/Machine-Learning/Rekognition.svg"></a>Rekognition</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Amazon Bedrock" height="20" width="20" style="margin-right: 10px" src="https://www.outsystems.com/Forge_CW/_image.aspx/Q8LvY--6WakOw9afDCuuGQ_Q2qNoQaT-xrNXdmgM4dI=/aws-bedrock-connector-2023-01-04%2000-00-00-2024-04-11%2006-34-50"></a>Amazon Bedrock</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Amazon CloudWatch" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/AWS/svg/Management-Governance/CloudWatch.svg"></a>CloudWatch</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Amazon S3 Bucket" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/AWS/svg/Storage/Simple-Storage-Service.svg"></a>S3 Bucket</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Lambda" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/AWS/svg/Compute/Lambda.svg"></a> AWS Lambda</td>
        <td>Current</td>
    </tr>
    <tr>
        <td> <a href=""><img align="left" alt="Python" height="20" width="20" style="margin-right: 10px" src="https://icon.icepanel.io/Technology/svg/Python.svg"></a> Python</td>
        <td>V. 3.9</td>
    </tr>
    </tr>
  </table>
</div>

***

## 📍 Rotas da Aplicação

1. O status code para sucesso das requisições será `200`
2. As imagens passadas nos métodos POST devem estar nos formatos `.jpg` ou `.png`, estando armazenada em um bucket S3.

***

### Rota 1 → GET `/` 

```json 
   { 
     "message": "Go Serverless v3.0! Your function executed successfully!", 
     "input": { 
         ...(event) 
     } 
   } 
```
  
### Rota 2 → GET `/v1`

```json 
{ 
   "message": "VISION api version 1." 
} 
```
  
### Rota 3 → GET `/v2`
  
```json 
{ 
   "message": "VISION api version 2." 
} 
```
***
### POST

Ambas as rotas POST recebem uma requisição no formato:
```json  
{  
   "bucket": "myphotos",  
   "imageName": "image.jpg"
}  
```

### Rota 4 -> POST `/v1/vision`

- Retorno esperado:

```json
{
    "url_to_image": "https://bucket-test-sls.s3.amazonaws.com/mulher.jpg",
    "created_image": "03-05-2024 17:05:34",
    "faces": [
        {
            "position": {
                "top": 0.03809963911771774,
                "left": 0.22477570176124573,
                "width": 0.3694091737270355,
                "height": 0.704017698764801
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 98.046875
        }
    ]
}
```

### Rota 5 -> POST `/v2/vision`

- Retorno esperado:

```json  
{
    "url_to_image": "https://bucket-test-sls.s3.amazonaws.com/pug.jpg",
    "created_image": "07-05-2024 22:08:51",
    "labels": [
        {
            "Confidence": 99.29735565185547,
            "Name": "Animal"
        },
        {
            "Confidence": 99.29735565185547,
            "Name": "Dog"
        },
        {
            "Confidence": 99.29735565185547,
            "Name": "Pet"
        },
        {
            "Confidence": 97.89754486083984,
            "Name": "Pug"
        }
    ],
    "Dicas": "Dicas sobre Pugs:  Nível de Energia e Necessidades de Exercícios: Pugs são de nível médio de energia, necessitando de 30 minutos de exercício por dia.  Temperamento e Comportamento: Cariñosos, alegres, inteligentes e dependentes de pessoas.  Cuidados e Necessidades: Pelos curtos e finos que precisam de cuidados especializados, como lavagem regular e penteado. A alimentação deve ser balanceada, comercial ou homemade, ajustando a quantidade conforme o peso do cão.  Problemas de Saúde Comuns: Arritmia cardíaca, hipoacusia, luxação da coluna e problemas respiratórios."
}
```

***

## 🚀 Como executar o projeto

É possível utilizar o sistema de duas formas distintas, por meio de sua implementação na plataforma da AWS, localmente, ou em ambiente de produção utilizando o link disponibilizado.

### Utilizando em ambiente de produção

1. Acesse o endpoint da API por meio do link:

```
  https://oxz3hdtxx1.execute-api.us-east-1.amazonaws.com
```

2. Faça requisições às rotas seguindo o modelo e teste as respostas fornecidas.

### Executando localmente

1. Clone o repositório do GitHub em sua máquina local:

```
  git clone -b grupo-6 https://github.com/Compass-pb-aws-2024-IFSUL-UFERSA/sprint-8-pb-aws-ifsul-ufersa
```

2. Instale o serverless

```
  npm install -g serverless
```

3. Navegue até pasta em que se encontra a aplicação e execute o seguinte comando para iniciá-la:

```
  serverless deploy
```

4. Faça requisições às rotas fornecidas seguindo o modelo e teste as respostas retornadas.
***

## 👩🏽‍💻 Desenvolvimento

O projeto foi desenvolvido utilizando a linguagem Python, juntamente do framework Serverless.

A API faz uso de algumas ferramentas da AWS em seu funcionamento, como o Rekognition, o Bedrock, o Cloudwatch e a Amazon Lambda.

Iniciamos delegando as funções para os membros da equipe, definindo qual membro ficaria com determinada rota, após isso foram feitos alguns testes para verificar o funcionamento da aplicação.

### Estrutura AWS

![Estrutura de Cloud na AWS](./assets/arquitetura-base.jpg)

***

## 📁 Organização das Pastas

![Estrutura de Pastas](./assets/FolderStructure.png)

***

## 🚨 Dificuldades Conhecidas

Entre as dificuldades enfrentadas pela equipe ao longo do desenvolvimento do projeto, notamos:

- Dificuldade inicial em delegar tarefas para cada integrante.
- Problemas para desenvolver um prompt que possa gerar a melhor resposta possível.

***

## 👷🏾 Desenvolvedores

- [Juhan Freitas](https://github.com/juhanfreitas)
- [Pablo Lucas](https://github.com/Pablosxz)
- [Ricardo Dall'Agnol](https://github.com/Richoland)
- [Thiago Coelho](https://github.com/thiagocoelhoo)
