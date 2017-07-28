#! /usr/bin/python

import boto3, datetime, time, sys, csv, json,urllib2,string,os
stamp = datetime.datetime.now().strftime('%Y-%m-%d')
report_dir=datetime.datetime.now().strftime('%Y-%m-%d')
regions = [ 'ap-northeast-1','ap-southeast-1','ap-southeast-2','eu-central-1','eu-west-1','sa-east-1','us-east-1','us-west-1','us-west-2']
data = []
for az in regions:
        ec2 = boto3.client('ec2',region_name=az) # via pre assumed IAM ROLE on instance OR use aws key secret.
        #ec2 = boto3.client('ec2',aws_access_key_id = 'access key',aws_secret_access_key = 'secretkey',region_name=az) 
        ids = ec2.describe_instances()
        for instances in ids['Reservations']:
                running=[]
                try: running.append(instances['Instances'][0]['Placement']['AvailabilityZone']) 
                except KeyError: running.append('_')
                running.append(instances['Instances'][0]['InstanceId']) 
                running.append(instances['Instances'][0]['Tags'][0]['Value']) 
                running.append(instances['Instances'][0]['State']['Name'])
                running.append(instances['Instances'][0]['PrivateIpAddress'])
                running.append(instances['Instances'][0]['PrivateDnsName'])
                try: running.append(instances['Instances'][0]['VpcId'])
                except KeyError: running.append('_')
                running.append(instances['Instances'][0]['VirtualizationType'])
                try: running.append(instances['Instances'][0]['PublicIpAddress'])
                except KeyError: running.append('_')
                try: running.append(instances['Instances'][0]['PublicDnsName'])
                except KeyError: running.append('_')
                try: running.append(instances['Instances'][0]['Platform'])
                except KeyError: running.append('Linux')

                data.append(running)


os.popen('mkdir -p ./Reports/'+report_dir)
header = ['AvailabilityZone','InstanceId','TagName','StateName','PrivateIpAddress','PrivateDnsName','VpcId','VirtualizationType','PublicIpAddress','PublicDnsName','Platform']
f = open('./Reports/'+report_dir+'/instances-'+stamp+'.csv', 'w')
try:
        writer = csv.writer(f)
        writer.writerow( (header))
finally:
        f.close()

f = open('./Reports/'+report_dir+'/instances-'+stamp+'.csv', 'a')
try:
        writer = csv.writer(f)
        for values in sorted(data):
                writer.writerow(values)
finally:
        f.close()


