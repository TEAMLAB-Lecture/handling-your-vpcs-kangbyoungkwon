import boto3
import time
import csv
from botocore.exceptions import ClientError

f = open('test.csv', 'w')
ec2 = boto3.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

for i in range(10):
    try:
        response = ec2.create_security_group(GroupName='Hello'+str(i),
                                            Description='Made by boto3',
                                            VpcId='vpc-e7597e80')
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
        print('Ingress Successfully Set %s' % data)
        print(data['ResponseMetadata']['HTTPHeaders']['date'])

        f.write("%s,%s.\n" % (security_group_id, data['ResponseMetadata']['HTTPHeaders']['date']))
        time.sleep(5)

    except ClientError as e:
        f.write("%s.\n" % ('default create error'))
        print(e)
