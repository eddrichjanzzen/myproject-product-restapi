# Build a Python Flask Rest API Service using AWS ECS 
This project is a scaffold for a modern application using AWS. Follow the steps below to download, install and run this project.

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

## Module 1: Configure your Development Environment
Time to complete: 5 minutes

### Step 1.1: Create Environment Working Directory
```
$ mkdir environment
$ cd ~/environment
```

### Step 1.2: Clone Github Repository and change directory
```
$ https://github.com/jrdalino/modern-app-workshop.git
$ cd modern-web-workshop