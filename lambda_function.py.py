import json
import boto3
import csv
import uuid  # Generate unique IDs if needed
from datetime import datetime

# ✅ Replace these with your actual AWS resource names
S3_BUCKET_NAME = "csv-arya"
DYNAMODB_TABLE_NAME = "dynamo"
SNS_TOPIC_ARN = "arn:aws:sns:us-west-2:654654201955:arya"  # ✅ Replace with your SNS Topic ARN

# ✅ Initialize AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")  # ✅ SNS Client
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))  # ✅ Debugging

    try:
        # ✅ Extract bucket name and object key from event
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]

        print(f"Processing file: {object_key} from bucket: {bucket_name}")

        # ✅ Fetch file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8").splitlines()

        # ✅ Process CSV file
        csv_reader = csv.DictReader(file_content)

        # ✅ Store each row in DynamoDB
        item_count = 0
        for row in csv_reader:
            row["id"] = str(row["id"])  # Ensure id is a string
            row["age"] = int(row["age"])  # Convert age to number

            print("Inserting row:", row)
            table.put_item(Item=row)
            item_count += 1

        # ✅ Send SNS notification after successful processing
        message = f"CSV file '{object_key}' processed successfully.\nTotal rows inserted: {item_count}"
        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="CSV Processing Complete")

        return {
            "statusCode": 200,
            "body": json.dumps("CSV rows stored & SNS notification sent!")
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # ✅ Debugging
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }
