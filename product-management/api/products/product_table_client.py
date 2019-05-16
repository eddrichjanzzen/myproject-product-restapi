import boto3
import json
import logging
from collections import defaultdict
import argparse
from decouple import config
import uuid
from custom_logger import setup_logger


logger = setup_logger(__name__)

# For production: 

# create a DynamoDB client using boto3. The boto3 library will automatically
# use the credentials associated with our ECS task role to communicate with
# DynamoDB, so no credentials need to be stored/managed at all by our code!

# For local development
# we need to specify the aws access keys to be random string

# dynamodb = boto3.client('dynamodb', 
#             endpoint_url=config('DYNAMODB_ENDPOINT_URL', default='http://dynamo-db:8000/'),
#             region_name=config('REGION', default='ap-southeast-1'),
#             aws_access_key_id='x',
#             aws_secret_access_key='x'
#         )

# table_name = config('TABLE_NAME', default='SampleTable')


# dynamodb = boto3.client('dynamodb')
# table_name = 'ProductTable'

def getJsonData(items):
    # create a default dictonary
    product_list = defaultdict(list)
    
    # loop through the items given as parameters
    for item in items:
    # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }
        product_list['products'].append(product)

    return product_list
    
def getAllProducts():

    response = dynamodb.scan(
        TableName=table_name
    )
        
    # loop through the returned dict and convert this into json
    data_list = getJsonData(response["Items"])
    
    return json.dumps(data_list)

# Retrive a single mysfit from DynamoDB using their unique mysfitId
def getProduct(product_id):

    # get a product by its unique key
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )


    # check if the item exists in dynamodb
    if 'Item' in response:
        item = response['Item']

        logger.info("Get Product Response: ")
        logger.info(response)
        
        # define product payload object
        product = {
            'id': item["id"]["S"],
            'name': item['name']['S'],
            'description': item['description']['S'],
            'image_url': item['image_url']['S'],
            'price': item['price']['N'],
        }

    else:

        product = {
            'status' : "The product with id: {} does not exist.".format(product_id)
        }


    return json.dumps(product)

def createProduct(product_dict):

    product_id = str(uuid.uuid4())
    product_name = str(product_dict['name'])
    product_description = str(product_dict['description'])
    product_image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])


    response = dynamodb.put_item(
        TableName=table_name,
        Item={
                'id': {
                    'S': product_id
                },
                'name': {
                    'S' : product_name
                },
                'description' : {
                    'S' : product_description
                },
                'image_url': {
                    'S' : product_image_url
                },
                'price': {
                    'N' : price
                }             
            }
        )

    # define product payload object

    product = {
        'id': item["id"]["S"],
        'name': item['name']['S'],
        'description': item['description']['S'],
        'image_url': item['image_url']['S'],
        'price': item['price']['N'],
        'status' : 'CREATED OK'
    }

    return json.dumps(product)

def updateProduct(product_id, product_dict):

    # TODO: Fix validation for record updates

    # example used for updating values
    # https://stackoverflow.com/questions/37721245/boto3-updating-multiple-values
    name = str(product_dict['name'])
    description = str(product_dict['description'])
    image_url = str(product_dict['image_url'])
    price = str(product_dict['price'])

    response = dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        },
        UpdateExpression="""SET name = :p_name, 
                                description = :p_description,
                                image_url = :p_image_url,
                                price = :p_price
                                """,
        ExpressionAttributeValues={
            ':p_name': {
                'S' : product_name
            },
            ':p_description' : {
                'S' : product_description
            },
            ':p_image_url': {
                'S' : image_url
            },
            ':p_image_url': {
                'N' : price
            }              
        }
    )


    logger.info("Update Product Response: ")
    logger.info(response)

    # define product payload object
    product = {
        'id': item["id"]["S"],
        'name': item['name']['S'],
        'description': item['description']['S'],
        'image_url': item['image_url']['S'],
        'price': item['price']['N'],
        'status' : 'UPDATED OK'
    }


    return json.dumps(product)

def deleteProduct(product_id):

    response = dynamodb.delete_item(
        TableName=table_name,
        Key={
            'id': {
                'S': product_id
            }
        }
    )

    product = {
        'id' : product_id,
        'status' : 'DELETED OK'
    }

    return json.dumps(product)
