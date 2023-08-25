import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')  # Change to your desired region
    name_filter = "*"

    response = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [name_filter]}])

    instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    for instance in instances:
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        status = instance['State']['Name']
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        public_ip = instance.get('PublicIpAddress', 'N/A')
        tags = instance.get('Tags', [])
        for tag in tags:
            if tag['Key'] == 'Name':
                instance_name = tag['Value']
                break
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])['Volumes']
        total_size_ebs_volumes = sum(vol['Size'] for vol in volumes)

        print("Instance ID:", instance_id)
        print("Instance Type:", instance_type)
        print("Status:", status)
        print("Private IP:", private_ip)
        print("Public IP:", public_ip)
        print("Total Size Ebs Volumes:", total_size_ebs_volumes)
        print("Instance Name:", instance_name)
        print("---")

if __name__ == '__main__':
    lambda_handler(event, context)
