# COCUS-DEVOPS-TEST

<img width="964" alt="image" src="https://github.com/FavourOkonta/cocus-devops-test/assets/71400388/604f9191-746a-44e5-8174-fb9c27d02d30">


A Devops test to implement a Python3 script using boto3 and AWS

There are few servers running in the AWS account.
This account is accessed using a provided AccessKey and SecretKey ID.

The cocus.py script has been provided as a solution to the exercise given; and then zipped into the cocus.zip file.

The cocus.py script aims at searching for Instances and their details by inputting the EC2 server Name (tag) or searching for
all of them (by giving input '*' ). It also returns a table with a list of fields for each server:
instance-id, instance-type, status, private-ip, public-ip (if available) and total-size-ebs-volumes.

Furthermore, it goes ahead to provide a list of all servers ordered by the total size of EBS volumes attached.
The Tag: True/False can be toggled to switch the ordering to be in an ascending format/descending format.

Lastly, the script prints out the total size of all the EBS volumes in GB of all servers.



TASK-SPECIFIC PARAMETERS
ACCESS KEY: **see attached mail**
SECRET KEY: **see attached mail**
REGION: eu-central-1



**MANUAL DEPLOYMENT STEPS**

1. Input the provided AWS ACCESS KEY AND SECRET KEY CREDENTIALS (either as an ENV variable)

2. Package the respective python script into a .zip file (This would be referenced for deployment on Lambda)
             zip -r cocus.zip cocus.py

3. Initialize your Terraform configuration in the folder
             Terraform init

4. With the main.tf and provider.tf files properly configured, run terraform plan
              Terraform plan

5. Finally deploy the AWS resources that create: a lambda function, a new role, and a role attachment.
             Terraform apply


**CI-CD ACTION**
A Github workflow file has also been attached for automatic triggers from the main branch with environment variables looked up.
