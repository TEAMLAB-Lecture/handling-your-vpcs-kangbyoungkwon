import boto3
import csv
import datetime
import time
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

result = ec2.describe_security_groups()

#with open('test.csv', 'w') as f:
deleted_groupId = []
#print(result['GroupId'])
with open('test.csv', 'a') as f:
    for i in range(10):
        for value in result["SecurityGroups"]:
        #print(value["GroupName"])
            if value["GroupName"] == 'Hello'+str(i):
                try:
                    response = ec2.delete_security_group(GroupName = value["GroupName"])
                    print(response)
                    print("Security Group Deleted")
                    deleted_groupId.append(value["GroupId"])
                    #with open('test.csv', 'w') as f:
                    f.write("%s,%s.\n" % (value["GroupId"], datetime.datetime.now()))
                    time.sleep(5)

                except ClientError as e:
                    f.write("%s.\n" % ('default delete error'))
                    print(e)

print (deleted_groupId)

#원래 있던 csv 파일 열어서 거기다 덮어쓰는 것부터 시작
