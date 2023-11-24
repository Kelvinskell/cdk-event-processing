import json
import random
import string
import boto3

# Connect to dynamodb
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('employee-info')


def lambda_handler(event, context):
    
    # Log evnt body to Cloudwatch
    workId = event['Records'][0]['body']
    print(workId)
    
    # Generate secretId
    characters = string.ascii_letters + string.digits + string.punctuation
    secret = ''.join(random.choice(characters) for i in range(8))
    secretId = secret

    # Write to Dynamodb
    table.put_item(
        Item={
            'workId': workId,
            'secretId': secretId
        }
    )
    
    # return statusCode
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }