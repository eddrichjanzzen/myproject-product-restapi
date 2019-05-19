import os
import uuid
from flask import Blueprint
from flask import Flask, json, Response, request
from custom_logger import setup_logger

# Set up the custom logger and the Blueprint
logger = setup_logger(__name__)
product_module = Blueprint('products', __name__)


logger.info("Intialized product routes")

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'products.json')

# load products static db from json file
with open(my_file) as f:
    products = json.load(f)


# Allow the default route to return a health check
@product_module.route('/')
def health_check():
    return "This a health check. Product Management Service is up and running."

    
@product_module.route('/products')
def get_all_products():

    #returns all the products coming from dynamodb
    serviceResponse = json.dumps({'products': products})
    
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    
    return resp
    
@product_module.route("/products/<product_id>", methods=['GET'])
def get_product(product_id):

    #returns a product given its id
    serviceResponse = json.dumps({'products': products[0]})

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products", methods=['POST'])
def create_product():

    product_dict = json.loads(request.data)

    product = {
        'product_id': str(uuid.uuid4()),
        'name': product_dict['name'],
        'description': product_dict['description'],
        'image_url': product_dict['image_url']
    }


    serviceResponse = json.dumps({'products': product})
    resp = Response(serviceResponse)

    resp.headers["Content-Type"] = "application/json"

    return resp


@product_module.route("/products/<product_id>", methods=['PUT'])
def update_product(product_id):
    
       #creates a new product. The product id is automatically generated.
    product_dict = json.loads(request.data)

    products[0]['name'] = request.json.get('name', products[0]['name'])
    products[0]['description'] = request.json.get('description', products[0]['description'])
    products[0]['image_url'] = request.json.get('image_url', products[0]['image_url'])
    
    serviceResponse = json.dumps({'products': products[0]})

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    
    #deletes a product given its id.
    serviceResponse = json.dumps({"products" : "Deletes a product with id: {}".format(product_id)})

    products.remove(products[0])

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

