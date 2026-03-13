import json
import os
import time
import urllib.request
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    plot_api_url = os.environ['PLOT_API_URL']

    s3.put_object(
        Bucket=bucket_name,
        Key="assignment1.txt",
        Body="Empty Assignment 1",
        ContentType="text/plain",
    )
    time.sleep(2)

    s3.put_object(
        Bucket=bucket_name,
        Key="assignment1.txt",
        Body="Empty Assignment 2222222222",
        ContentType="text/plain",
    )
    time.sleep(2)

    s3.delete_object(
        Bucket=bucket_name,
        Key="assignment1.txt",
    )
    time.sleep(2)

    s3.put_object(
        Bucket=bucket_name,
        Key="assignment2.txt",
        Body="33",
        ContentType="text/plain",
    )
    time.sleep(2)

    with urllib.request.urlopen(plot_api_url) as response:
        api_body = response.read().decode('utf-8')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'plot_api_response': api_body,
        })
    }