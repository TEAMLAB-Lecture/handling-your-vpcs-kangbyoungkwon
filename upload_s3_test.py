import uuid
import boto3
import os
import botocore

ss3 = boto3.resource('s3')
s3 = boto3.client('s3')
files = os.listdir("./")

response = s3.list_buckets()
randomString = str(uuid.uuid4()).replace("-","")
bucket_name = randomString
buckets = [bucket['Name'] for bucket in response['Buckets']]
KEY = 'test.csv'

if bucket_name not in buckets :
    print(bucket_name)
    s3 = boto3.client('s3', region_name="ap-southeast-1")
    creation = s3.create_bucket(
        Bucket= bucket_name, #버킷의 이름
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-1'
            }
        )
    files = os.listdir("./")
    for filename in files:
        s3.upload_file(filename, bucket_name, filename)

    try:
        ss3.Bucket(bucket_name).download_file(KEY, 'new_test.csv')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

        with open('test.csv', 'r') as f, open('new_test.csv','r') as f2 :
            first = f.readlines()
            second = f.readlines()
        with open('test.csv', 'a') as outfile:
            for i in second:
                if i not in first:
                    outfile.write(i)

        for filename in files:
            s3.upload_file(filename, bucket_name, filename)

        else:
            raise

else:
    print("bucket is already exist")
    files = os.listdir("./")
    for filename in files:
        s3.upload_file(filename, bucket_name, filename)
    try:
        ss3.Bucket(bucket_name).download_file(KEY, 'new_test.csv')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

        with open('test.csv', 'r') as f, open('new_test.csv','r') as f2 :
            first = f.readlines()
            second = f.readlines()

        with open('test.csv', 'a') as outfile:
            for i in second:
                if i not in first:
                    outfile.write(i)
                    
        for filename in files:
            s3.upload_file(filename, bucket_name, filename)
