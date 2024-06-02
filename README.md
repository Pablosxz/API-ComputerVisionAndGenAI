# Pet Emotion Detector and Tips Generator for Pet Owners


## 📃 Table of Contents

- [Project Scope](#-project-scope)
- [Tools and Technologies Used](#-tools-and-technologies-used)
- [Application Routes](#-application-routes)
- [How to Use the System](#-how-to-use-the-system)
- [Development](#-development)
- [License](#-license)



## 🔭 Project Scope

The API was developed to provide two distinct functionalities:

- Detect emotions in the faces present in the images sent as parameters.
- Detect the breed of animals in the photos sent, and generate tips to facilitate the care of your pets, whether they are health tips or behaviors that your pet may exhibit.



## 🛠️ Tools and Technologies Used

<div style="display: inline_block">
  <table border="1">
    <tr>
        <th>Technology</th>
        <th>Version</th>
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
  </table>
</div>


## 📍 Application Routes

1. The success status code for requests will be `200`.
2. The images passed in the POST methods must be in `.jpg` or `.png` format, stored in an S3 bucket.



### Route 1 → GET `/` 

```json 
   { 
     "message": "Go Serverless v3.0! Your function executed successfully!", 
     "input": { 
         ...(event) 
     } 
   } 
```
  
### Route 2 → GET `/v1`

```json 
{ 
   "message": "VISION API version 1." 
} 
```
  
### Route 3 → GET `/v2`
  
```json 
{ 
   "message": "VISION API version 2." 
}
```
***

### POST

Both POST routes receive a request in the format:
```json  
{  
   "bucket": "myphotos",  
   "imageName": "image.jpg"
}  
```

### Route 4 -> POST `/v1/vision`

- Expected return:

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

### Route 5 -> POST `/v2/vision`

- Expected return:

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
    "Dicas": "Tips about Pugs:  Energy Level and Exercise Needs: Pugs have a medium energy level, requiring 30 minutes of exercise per day.  Temperament and Behavior: Affectionate, cheerful, intelligent, and dependent on people.  Care and Needs: Short and fine hair that needs specialized care, such as regular washing and brushing. The diet should be balanced, whether commercial or homemade, adjusting the amount according to the dog's weight.  Common Health Problems: Cardiac arrhythmia, hearing loss, spinal dislocation, and respiratory problems."
}
```

***

## 🚀 How to Run the Project

You can use the system by implementing it on the AWS platform, locally.


### Running Locally

1. Clone the GitHub repository to your local machine:

```
  git clone ...
```

2. Install serverless

```
  npm install -g serverless
```

3. Navigate to the folder where the application is located and run the following command to start it:

```
  serverless deploy
```

4. Make requests to the provided routes following the model and test the returned responses.

***

## 👩🏽‍💻 Development

The project was developed using the Python language, along with the Serverless framework.

The API makes use of several AWS tools in its operation, such as Rekognition, Bedrock, Cloudwatch, and Amazon Lambda.

### AWS Structure

![Cloud Structure on AWS](./assets/arquitetura-base.jpg)


## 📜 License

This project is licensed under the terms of the MIT License. See the [LICENSE](./LICENSE) file for more details.
