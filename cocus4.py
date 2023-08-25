import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')  # Change to your desired region
    name_filter = "*"

    response = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [name_filter]}])

    instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    total_ebs_size_gb = 0

    for instance in instances:
        instance_id = instance['InstanceId']
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])['Volumes']
        total_size_ebs_volumes = sum(vol['Size'] for vol in volumes)
        total_ebs_size_gb += total_size_ebs_volumes

    print(f"Total size of all EBS volumes: {total_ebs_size_gb} GB")

if __name__ == '__main__':
    lambda_handler(event, context)
