
# Backend Python Flask RestAPI  

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

The Backend Project Layout will look like this:

```
~/environment/python-restapi-service
├── README.md
├── aws-cli
└── product-management
    ├── Dockerfile
    ├── api
    │   ├── app.py
    │   ├── custom_logger.py
    │   └── products
    │       └── product_routes.py
    └── requirements.txt
```

## Step 1: Create Backend using Python Flask REST API
-  Create basic CRUD functionality for a product-management service
- The Service will be triggered by developers via a web api
```
| HTTP METHOD | URI                                     | ACTION                      |
|-------------|-----------------------------------------|-----------------------------|
| GET         | http://[hostname]/products              | Gets all products           |
| GET         | http://[hostname]/products/<product_id> | Gets one product            |
| POST        | http://[hostname]/products              | Creates a new product       |
| PUT         | http://[hostname]/products/<product_id> | Updates an existing product |
| DELETE      | http://[hostname]/products/<product_id> | Deletes a product           |
```

### Step 1.1: Create a CodeCommit Repository
```
$ aws codecommit create-repository --repository-name Product-Managment-Svc-Repo
```

### Step 1.2: Clone the repository
```
$ cd ~/environment
$ git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/Product-Managment-Svc-Repo
```

### Step 1.3: Copy CRUD template into contents into the code commit repository
```
$ cp -r ~/environment/python-restapi-service/product-management/* ~/environment/python-restapi-service/Product-Managment-Svc-Repo/
$ git add .
$ git commit -m "Copy CRUD template into codecommit repository
$ git push origin master
```

### Step 1.4: Navigate to working directory
```
$ cd ~/environment/Product-Management-Svc-Repo
$ python3 -m venv venv
$ source venv/bin/activate
$ venv/bin/pip install flask
$ venv/bin/pip install flask-cors
```
### Step 1.5: Run Locally and Test
```
$ cd ~/environment/Product-Management-Svc-Repo/api
$ python app.py
$ curl http://localhost:8080
```

### Step 1.10: Backend Unit Tests
Todo

### Step 1.11: Create the Dockerfile
```
$ cd ~/environment/Product-Management-Svc-Repo  
$ vi Dockerfile
```
```
# Set base image to python
FROM python:3.6

ENV PYTHONBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . /code/

WORKDIR /code/api

EXPOSE 8080

ENTRYPOINT ["python"]

CMD ["app.py"]
```

### Step 1.13: Build, Tag and Run the Docker Image locally
Replace:
- AccountId: 707538076348
- Region: us-east-1

```
$ docker build -t product-management-service .
$ docker tag product-management-service:latest 707538076348.dkr.ecr.us-east-1.amazonaws.com/product-management-service:latest
$ docker run -p 8000:8000 product-management-service:latest
```

### Step 1.15: Test CRUD Operations
- Test Get all Products
```
curl -X GET \
  http://localhost:8080/products \
  -H 'Host: localhost:8080'
```
```
{"response": "Gets all products", "test": "test"}
```
- Test Get Product
```
curl -X GET \
  http://localhost:8080/products/d58ada00-1d53-4164-9453-b8fe3fb080c5 \
  -H 'Host: localhost:8080' 
```
```
{"response": "Gets a product with id d58ada00-1d53-4164-9453-b8fe3fb080c5"}
```
- Test Create Product
```
curl -X POST \
  http://localhost:8080/products \
  -H 'Host: localhost:8080' \
  -H 'Content-Type: application/json' \
  -d '{
    "product_name":"Product G",
    "product_description": "Nulla nec dolor a ipsum viverra tincidunt eleifend id orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.",
    "product_image_url": "https://via.placeholder.com/200"
}'
```
```
{  
"body":{  
"product_description":"Nulla nec dolor a ipsum viverra tincidunt eleifend id orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.",  
"product_image_url":"https://via.placeholder.com/200",  
"product_name":"Product G"  
},  
"response":"Creates a new product."  
}
```
- Test Update Product
```
curl -X PUT \
  http://localhost:8080/products/d58ada00-1d53-4164-9453-b8fe3fb080c5 \
  -H 'Content-Type: application/json' \
  -d '{
    "product_name":"egg 123",
    "product_description": "my working description dasdasds",
    "product_image_url": "product_image testes update test"
}'
```
```
{  
"body":{  
"product_description":"my working description dasdasds",  
"product_image_url":"product_image testes update test",  
"product_name":"egg 123"  
},  
"response":"Updates an existing product"  
}
```

- Test Delete Product
```
curl -X DELETE \
  http://localhost:8080/products/b130f58b-c700-4bde-bad7-a1218ce60ccb \
  -H 'Content-Type: application/json' 
```
```
{  
"response":"Deletes a product with id: b130f58b-c700-4bde-bad7-a1218ce60ccb"  
}
```

### Step 1.16: Create the ECR Repository
```
$ aws ecr create-repository --repository-name Product-Management-Svc
```

### Step 1.17: Run login command to retrieve credentials for our Docker client and then automatically execute it (include the full command including the $ below).
```
$ $(aws ecr get-login --no-include-email)
```

### Step 1.18: Push our Docker Image
```
$ docker push 707538076348.dkr.ecr.us-east-1.amazonaws.com/product-management-service:latest
```

### Step 1.19: Validate Image has been pushed
```
$ aws ecr describe-images --repository-name product-management-service
```

### (Optional) Clean up
```
$ aws ecr delete-repository --repository-name product-management-service --force
$ aws codecommit delete-repository --repository-name Product-Management-Svc-Repo
$ rm -rf ~/environment/Product-Management-Svc-Repo
```
