
# Build a Python Flask REST API Service using AWS ECS 

This project is a scaffold for building a REST API service using AWS ECS. Follow the steps below to download, install and run this project. 

The Project Layout will look like this:
```
|____aws-cli
| |____core.yaml
|____product-management
| |____docker-compose.yaml
| |____requirements.txt
| |____Dockerfile
| |____buildspec.yml
| |____.gitignore
| |____api
| | |____products
| | | |____product_table_client.py
| | | |____product_routes.py
| | |____custom_logger.py
| | |____app.py
```
## Prerequsites
- AWS Account
- IAM User with Administrator Access and Access Keys
- AWS CLI
```
$ aws --version
aws-cli/1.16.8 Python/2.7.10 Darwin/16.7.0 botocore/1.11.8
```
- Git
```
$ git --version
git version 2.14.3 (Apple Git-98)
```
- Python
```
$ python
Python 2.7.10 (default, Feb  7 2017, 00:08:15) 
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
- Docker
```
$ docker -v
Docker version 18.09.2, build 6247962
```

## Step 1: Configure your Development Environment
Time to complete: 5 minutes

### Step 1.1: Create Environment Working Directory
```
$ mkdir environment
$ cd ~/environment
```

### Step 1.2: Clone Github Repository and change directory
```
$ https://github.com/ejanzzenang/restapi-service-using-aws-ecs.git 
$ cd restapi-service-using-aws-ecs
```
## Step 2: Create the Core Infrastructure using AWS CloudFormation
Time to Complete: 10 minutes

Services Used: 
- AWS CloudFormation
- AWS Identity and Access Management (IAM)
- Amazon Virtual Private Cloud (VPC)

### Step 2.1: View/Modify the CloudFormation Stack
```
$ vi ~/environment/estapi-service-using-aws-ecs/aws-cli/core.yaml
```
This template will create:
- An Amazon VPC - a network environment that contains four subnets (two public and two private) in the 10.0.0.0/16 private IP space, as well as all the needed Route Table configurations. The subnets for this network are created in separate AWS Availability Zones (AZ) to enable high availability across multiple physical facilities in an AWS Region. Learn more about how AZs can help you achieve High Availability here.
- Two NAT Gateways (one for each public subnet, also spanning multiple AZs) - allow the containers we will eventually deploy into our private subnets to communicate out to the Internet to download necessary packages, etc.
- A DynamoDB VPC Endpoint - our microservice backend will eventually integrate with Amazon DynamoDB for persistence (as part of module 3).
- A Security Group - Allows your docker containers to receive traffic on port 8080 from the Internet through the Network Load Balancer.
- IAM Roles - Identity and Access Management Roles are created. These will be used throughout the workshop to give AWS services or resources you create access to other AWS services like DynamoDB, S3, and more.

### Step 2.2: Create the Stack
```
$ aws cloudformation create-stack \
--stack-name **<YOUR STACK NAME>** \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://environment/restapi-service-using-aws-ecs/aws-cli/core.yaml
```
Output:
```
{
    "StackId": "arn:aws:cloudformation:ap-southeast-1:486051038643:stack/MythicalMysfitsCoreStack/8a75e920-4426-11e9-90e7-0a04c4887732"
}
```


### Step 2.3: Check on the status of your stack until you see a status of "StackStatus": "CREATE_COMPLETE" 
```
$ aws cloudformation describe-stacks \
--stack-name MythicalMysfitsCoreStack
```

Output:

```
{
    "Stacks": [
        {
            "StackId": "arn:aws:cloudformation:ap-southeast-1:486051038643:stack/MythicalMysfitsCoreStack/8a75e920-4426-11e9-90e7-0a04c4887732", 
            "Description": "This stack deploys the core network infrastructure and IAM resources to be used for a service hosted in Amazon ECS using AWS Fargate.", 
            "Tags": [], 
            "EnableTerminationProtection": false, 
            "CreationTime": "2019-03-11T17:53:13.411Z", 
            "Capabilities": [
                "CAPABILITY_NAMED_IAM"
            ], 
            "StackName": "MythicalMysfitsCoreStack", 
            "NotificationARNs": [], 
            "StackStatus": "CREATE_IN_PROGRESS", 
            "DisableRollback": false, 
            "RollbackConfiguration": {}
        }
    ]
}
```

## Module 2: Deploy a Service with AWS ECS (Fargate)
Time to Complete: 30 minutes

Services Used: 
- AWS Elastic Container Registry (ECR)
- Amazon Elastic Container Service (ECS)
- AWS Fargate
- Amazon Elastic Load Balancing

### Step 2.1: View/Modify the Python Flask Code
```
# For the individual routes for CRUD Operations
$ vi ~/environment/restapi-service-using-aws-ecs/product-management/api/products/product_routes.py

# For dynamodb connectivity
$ vi ~/environment/restapi-service-using-aws-ecs/product-management/api/products/product_table_client.py
```

### Step 2.2: Navigate to application directory
```
$ cd ~/environment/modern-app-workshop/product-management
```

### Step 2.3: Build and Tag the Docker Image
Replace
- Accountid: 486051038643
- Region: ap-southeast-1
```
$ docker build . -t REPLACE_ME_ACCOUNT_ID.dkr.ecr.REPLACE_ME_REGION.amazonaws.com/product-management/service:latest
```

Output:
```
Sending build context to Docker daemon  49.15kB
Step 1/11 : FROM python:3
 ---> 59a8c21b72d4
Step 2/11 : ENV PYTHONBUFFERED 1
 ---> Using cache
 ---> 6858bd9192f9
Step 3/11 : RUN mkdir /code
 ---> Using cache
 ---> 28ddb0bde20f
Step 4/11 : WORKDIR /code
 ---> Using cache
 ---> 7111a3ab32e0
Step 5/11 : ADD requirements.txt /code/
 ---> Using cache
 ---> 274cb081599c
Step 6/11 : RUN pip install --upgrade pip
 ---> Using cache
 ---> 42069497f17b
Step 7/11 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 9eb709affa44
Step 8/11 : ADD . /code/
 ---> 211c69ed7e48
Step 9/11 : WORKDIR /code/api
 ---> Running in 1b839bb12666
Removing intermediate container 1b839bb12666
 ---> b58451188e87
Step 10/11 : ENTRYPOINT ["python"]
 ---> Running in ed40174c601f
Removing intermediate container ed40174c601f
 ---> 9ccb254fe928
Step 11/11 : CMD ["app.py"]
 ---> Running in 70638462086c
Removing intermediate container 70638462086c
 ---> b4a0af584ada
Successfully built b4a0af584ada
Successfully tagged 486051038643.dkr.ecr.ap-southeast-1.amazonaws.com/product-management/service:latest
```

### Step 2.4: Test the Service Locally
Replace
- Docker Image Tag
```
$ docker run -p 8080:8080 REPLACE_ME_ACCOUNT_ID.dkr.ecr.REPLACE_ME_REGION.amazonaws.com/product-management/service:latest
```
In another terminal, run the ff:
```
$ curl http://0.0.0.0:8080/
```

If successful you will see a response from the service that returns. The health check below:
```
This a health check. Product Management Service is up and running.
```

Output:
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
172.17.0.1 - - [11/Mar/2019 18:02:46] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [11/Mar/2019 18:02:50] "GET /mysfits HTTP/1.1" 200 -		
```

### Step 2.5: Create the ECR Repository
```
$ aws ecr create-repository \
--repository-name product-management/service
```

Output:
```
{
    "repository": {
        "registryId": "486051038643", 
        "repositoryName": "product-management/service", 
        "repositoryArn": "arn:aws:ecr:ap-southeast-1:486051038643:repository/mythicalmysfits/service", 
        "createdAt": 1552327411.0, 
        "repositoryUri": "486051038643.dkr.ecr.ap-southeast-1.amazonaws.com/product-management/service"
    }
}
```

### Step 2.6: Run login command to retrieve credentials for our Docker client and then automatically execute it (include the full command including the $ below).
```
$ $(aws ecr get-login --no-include-email)
```

Output:
```
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded
```


### Step 2.7: Push our Docker Image
Replace:
- Docker Image Tag
```
$ docker push 486051038643.dkr.ecr.ap-southeast-1.amazonaws.com/product-management/service:latest
```

Output:
```
The push refers to repository [486051038643.dkr.ecr.ap-southeast-1.amazonaws.com/product-management/service]
7baa9ad66120: Pushed 
4ec89687bef0: Pushed 
08402a185be9: Pushed 
3bc3d49b719b: Pushed 
96f710a2f207: Pushed 
4b7d93055d87: Pushed 
663e8522d78b: Pushed 
283fb404ea94: Pushed 
bebe7ce6215a: Pushed 
latest: digest: sha256:9f17e7b352653f67d13c6285466c7b6b887c0cc1aad817bb2fb1fd329087c2c2 size: 2206
```

### Step 2.8: Validate Image has been pushed
```
$ aws ecr describe-images \
--repository-name product-management/service
```

Output:
```
{
    "imageDetails": [
        {
            "imageSizeInBytes": 197410178, 
            "imageDigest": "sha256:9f17e7b352653f67d13c6285466c7b6b887c0cc1aad817bb2fb1fd329087c2c2", 
            "imageTags": [
                "latest"
            ], 
            "registryId": "486051038643", 
            "repositoryName": "product-managment/service", 
            "imagePushedAt": 1552327535.0
        }
    ]
}
```