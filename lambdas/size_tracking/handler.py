import os
import time
from datetime import datetime, timezone
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    table_name = os.environ['TABLE_NAME']

    table = dynamodb.Table(table_name)

    total_size_bytes = 0
    total_object_count = 0

    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            total_size_bytes += obj['Size']
            total_object_count += 1

    timestamp_epoch_ms = int(time.time() * 1000)
    timestamp_iso = datetime.now(timezone.utc).isoformat()

    table.put_item(
        Item={
            "bucket_name": bucket_name,
            "timestamp_epoch_ms": timestamp_epoch_ms,
            "timestamp_iso": timestamp_iso,
            "total_size_bytes": total_size_bytes,
            "total_object_count": total_object_count,
            "gsi1pk": "any name here works anyway"
        }
    )

    return {
        "statusCode": 200,
        "body": "ok"
    }