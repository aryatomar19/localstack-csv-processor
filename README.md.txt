# AWS Lambda CSV Processing with S3, DynamoDB, and SNS

## 📌 Project Overview
This project implements an **AWS Lambda function** that processes CSV files uploaded to an **S3 bucket**, extracts metadata and row data, stores it in **DynamoDB**, and sends a notification using **AWS SNS** upon successful processing.

---

## 🛠️ AWS Services Used
- **Amazon S3** → Stores uploaded CSV files.
- **AWS Lambda** → Processes CSV files upon S3 upload.
- **Amazon DynamoDB** → Stores extracted data.
- **Amazon SNS** → Sends notifications upon processing completion.

---

## 🚀 How It Works
1. **Upload a CSV file** to an S3 bucket.
2. **S3 Event triggers Lambda**, passing the file details.
3. **Lambda reads the CSV**, extracts metadata and row data.
4. **Each row is stored in DynamoDB**.
5. **SNS Notification is sent** upon successful processing.

---

## 📂 Project Structure
```
📁 aws-csv-processing
│── lambda_function.py  # AWS Lambda function code
│── users.csv           # Sample CSV file
│── README.md           # Project documentation
```

---

## 📌 AWS Lambda Function Code
```python
import json
import boto3
import csv
from datetime import datetime

S3_BUCKET_NAME = "your-bucket-name"  # Replace with actual bucket name
DYNAMODB_TABLE_NAME = "your-table-name"  # Replace with actual table name
SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:your-topic-name"  # Replace with actual ARN

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    try:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]

        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8").splitlines()
        csv_reader = csv.DictReader(file_content)

        item_count = 0
        for row in csv_reader:
            row["id"] = str(row["id"])
            row["age"] = int(row["age"])
            table.put_item(Item=row)
            item_count += 1

        message = f"CSV file '{object_key}' processed successfully. Total rows: {item_count}"
        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="CSV Processing Complete")

        return {"statusCode": 200, "body": json.dumps("CSV stored & SNS sent!")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
```

---

## 📌 Sample CSV File (users.csv)
```
id,name,age,city,date
1,Aryan,25,Bangalore,2025-03-05
2,Neha,30,Delhi,2025-03-04
3,Rahul,28,Mumbai,2025-03-03
4,Priya,22,Kolkata,2025-03-02
5,Varun,27,Chennai,2025-03-01
```

---

## 🔧 How to Deploy & Test
### **1️⃣ Set Up AWS Resources**
- **Create an S3 bucket** (`your-bucket-name`)
- **Create a DynamoDB table** (`your-table-name`) with `id` as the primary key
- **Create an SNS topic** and subscribe to it

### **2️⃣ Deploy Lambda Function**
1. Go to **AWS Lambda** → **Create a function**
2. Choose **Python 3.x** as runtime
3. Upload `lambda_function.py`
4. Set **Execution Role** with permissions:
   - `AmazonS3FullAccess`
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
5. Save & Deploy

### **3️⃣ Test the Function**
1. Upload `users.csv` to your S3 bucket
2. Check DynamoDB for stored data
3. Verify SNS notifications

---

## 📌 Expected SNS Notification
**Subject:** `CSV Processing Complete`
**Message:**
```
CSV file 'uploads/users.csv' processed successfully.
Total rows inserted: 5
```

---

## 📌 How to Submit
### **1️⃣ GitHub Repository Submission**
```bash
git init
git add .
git commit -m "Upload AWS CSV Processing Project"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```
Submit the **GitHub repository link**.

### **2️⃣ ZIP File Submission**
1. Compress the project folder as `aws_csv_processing.zip`
2. Upload it to your assignment portal

### **3️⃣ Direct AWS Lambda Submission** (If required)
- Go to AWS Lambda → Copy the **Function ARN**
- Submit the **Function ARN**

---

## 🎯 Conclusion
This project successfully processes CSV files in AWS, stores data in **DynamoDB**, and sends **SNS notifications**. 🚀

