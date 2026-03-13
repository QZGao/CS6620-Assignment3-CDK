import json
import os
import time
import boto3
import matplotlib
from boto3.dynamodb.conditions import Key
matplotlib.use('Agg')
import matplotlib.pyplot as plt

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    table_name = os.environ['TABLE_NAME']

    table = dynamodb.Table(table_name)

    now_epoch_ms = int(time.time() * 1000)
    start_epoch_ms = now_epoch_ms - 10 * 1000

    recent_records = table.query(
        KeyConditionExpression=Key('bucket_name').eq(bucket_name) & Key('timestamp_epoch_ms').between(start_epoch_ms, now_epoch_ms)
    ).get('Items', [])

    max_records = table.query(
        IndexName='global_max_size_index',
        KeyConditionExpression=Key('gsi1pk').eq('GLOBAL_MAX'),
        ScanIndexForward=False,
        Limit=1
    ).get('Items', [])
    global_max_size_bytes = int(max_records[0]['total_size_bytes']) if max_records else 0

    recent_records.sort(key=lambda x: int(x['timestamp_epoch_ms']))
    X = [int(item['timestamp_epoch_ms']) for item in recent_records]
    Y = [int(item['total_size_bytes']) for item in recent_records]

    plt.figure()
    if X:
        plt.plot(X, Y, marker='o')
    plt.axhline(global_max_size_bytes, color='r', linestyle='--', label='Historical high')
    plt.xlabel('Timestamp (epoch ms)')
    plt.ylabel('Size (bytes)')
    plt.title('Bucket size history in last 10s')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig("/tmp/plot.png", bbox_inches='tight')
    plt.close()

    s3.upload_file(
        "/tmp/plot.png",
        bucket_name,
        "plot",
        ExtraArgs={'ContentType': 'image/png'}
    )

    return {
        'statusCode': 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "Plot created successfully",
            "sample_point_count": len(X),
            "global_max_size_bytes": global_max_size_bytes
        })
    }