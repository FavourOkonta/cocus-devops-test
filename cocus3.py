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
            'instance-id': instance_id,
            'instance-type': instance_type,
            'status': status,
            'private-ip': private_ip,
            'public-ip': public_ip,
            'instance-name': instance_name,
            'total-size-ebs-volumes': total_size_ebs_volumes
        })

    # Sort instances by the total size of EBS volumes attached
    sorted_instances = sorted(instance_details, key=lambda x: x['total-size-ebs-volumes'], reverse=True) # True for Descending while False for Ascending

    # Now you can format and display the sorted instance details as a table
    for instance in sorted_instances:
        print(instance)  # You can format this output as a table or in any way you prefer

if __name__ == '__main__':
    lambda_handler(event, context)
