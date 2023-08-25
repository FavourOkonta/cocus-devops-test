import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')  # Change to your desired region
    name_filter = "*"

    response = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [name_filter]}])

    instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    instance_details = []

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

        instance_details.append({
            'instance_id': instance_id,
            'instance_type': instance_type,
            'status': status,
            'private_ip': private_ip,
            'public_ip': public_ip,
            'total_size_ebs_volumes': total_size_ebs_volumes,
            'instance_name': instance_name
        })

    # Sort instances by the total size of EBS volumes attached in ascending order
    sorted_instances = sorted(instance_details, key=lambda x: x['total_size_ebs_volumes'])

    for instance in sorted_instances:
        print("Instance ID:", instance['instance_id'])
        print("Instance Type:", instance['instance_type'])
        print("Status:", instance['status'])
        print("Private IP:", instance['private_ip'])
        print("Public IP:", instance['public_ip'])
        print("Total Size EBS Volumes:", instance['total_size_ebs_volumes'])
        print("Instance Name:", instance['instance_name'])
        print("---")
    
    total_ebs_size_gb = 0

    for instance in instances:
        instance_id = instance['InstanceId']
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])['Volumes']
        total_size_ebs_volumes = sum(vol['Size'] for vol in volumes)
        total_ebs_size_gb += total_size_ebs_volumes

    print(f"Total size of all EBS volumes: {total_ebs_size_gb} GB")

if __name__ == '__main__':
    lambda_handler(event, context)
