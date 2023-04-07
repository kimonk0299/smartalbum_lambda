
import json
import boto3
import time
import requests
#hello 
#hello

esUrl = "https://search-photos-rhflz75ugfgoilrjkiqlnzplbi.us-east-1.es.amazonaws.com/photoalbum/_doc"


def lambda_handler(event, context):
    jsonBody = event['Records'][0]
    bucketName = jsonBody['s3']['bucket']['name']
    key = jsonBody['s3']['object']['key']
    reko = boto3.client('rekognition')
    s3 = boto3.client('s3')
    try:
        data = {}
        responses3 = s3.head_object(Bucket = bucketName, Key =key )
        print("Bucket", bucketName)
        print("Key", key)
        print("Responses3", responses3)
        print("jsonBody", jsonBody)

        response = reko.detect_labels(
            Image={'S3Object': {'Bucket': bucketName, 'Name': key}})
        data['objectKey'] = key
        data['bucket'] = bucketName
        data['createdTimestamp'] = time.time()
        data['labels'] = []
        print("THIS is response")
        print(responses3)
        if not responses3['Metadata'] =={}:
            customlabel = responses3['Metadata']['customlabels']
            print("custom label below*")
            print(customlabel)
            if customlabel != "":
                data['labels'] = [i.strip() for i in customlabel.split(",")]

        for label in response['Labels']:
            if label['Confidence'] > 95:
                data['labels'].append(label['Name'])
        print(data['labels'])
        body = json.dumps(data)

        headers = {"Content-Type": "application/json"}
        r = requests.post(url=esUrl,auth = ('kishore', 'Test-12345'), data=body, headers=headers)
        
        print("all over")
    except Exception as e:
        print("Error " + str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
