# My Project Product Rest API

The folder structure will look like this:
```
~/environment/myproject-product-restapi
├── app.py
├── custom_logger.py
├── product_routes.py
├── products.json
├── requirements.txt
├── venv/
├── Dockerfile
├── README.md
└── .gitignore
```

## Step 1: Create Backend using Python Flask REST API
- Create basic CRUD functionality for a product-management service
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
```bash
$ aws codecommit create-repository --repository-name myproject-product-restapi
```

### Step 1.2: Clone the repository
```bash
$ cd ~/environment
$ git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/myproject-product-restapi
```

### Step 1.3: Set up .gitignore
```bash
$ cd ~/environment/myproject-product-restapi
$ vi .gitignore
```
```bash
# Byte-compiled / optimized / DLL files
__pycache__/
.api/__pycache__/
.api/products/__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Flask stuff:
instance/
.webassets-cache

# Virtual environment
venv
*.pyc

# IDE
.vscode
```

### Step 1.4: Test access to repo by adding README.md file and push to remote repository

```bash
$ cd ~/environment/myproject-product-restapi
$ echo "myproject-product-restapi" >> README.md
$ git add .
$ git commit -m "Adding README.md"
$ git push origin master
```

### Step 1.5: Set up virtual env
```bash
$ cd ~/environment/myproject-product-restapi
$ python3 -m venv venv
$ source venv/bin/activate
```

###  Step 1.6: Prepare static database
```bash
$ cd ~/environment/myproject-product-restapi
$ vi products_boracay.json
```
```json
[
  {
      "id":"4d196c50-aabf-4df2-afb3-fd21481259d6",
      "name":"Boracay Sunset Cruise",
      "description":"The Boracay sunset is a spectacular site to see and what better way than cruising on the ocean with an icy cold beverage!  Tour along White Beach and take in all the tropical sights and sounds while you enjoy the spectacular arrays of color of the Boracay sunset.  Stop off for a quick swim, stand up paddle and snorkel or chill out in tube before heading back to enjoy your dinner in paradise.",
      "image_url":"https://cdn5.myboracayguide.com/2019/02/Boracay-Sunset-Cruise-00-400x267.jpg",
      "price":"800"
  },
  {
      "id":"6b3c211a-53f3-4c2a-a4f3-dc1fd5d42bfc",
      "name":"Group Island Hopping",
      "description":"Make new friends by joining a shared boat cruise where you will cruise the shores of Boracay in a traditional Banka boat. Visit the famous Puka shell beach and take a stroll on the beach, swim in the azure waters or just relax with a fresh coconut enjoying the sun. Stop off for a snorkel and see Boracay\u2019s beautiful tropical fish and corals.  Finish the trip with a delicious buffet lunch.",
      "image_url":"https://cdn5.myboracayguide.com/2019/03/Boracay-Group-Island-Hopping-Boracay-Activities-01-400x267.jpg",
      "price":"1500"
  },
  {
      "id":"91e759dc-f385-42e1-8098-a44399bebce8",
      "name":"Ultimate Cliff Jumping Island Hopping Adventure",
      "description":"Experience a day of fun on Magic Island and have the thrill of a lifetime with 5 different levels of cliff jumping. Relax and swim or go snorkeling around the Island.",
      "image_url":"https://cdn5.myboracayguide.com/2016/06/Island-Hopping-Boracay-Activities-400x267-400x267.jpg",
      "price":"2200"
  },
  {
      "id":"2178bb44-32f1-4d22-bc95-05cd039a3067",
      "name":"4 Hour Private Boracay Island Hopping Package",
      "description":"Your Boracay adventure experience will not be complete without this trip! The island is home to more than a dozen undeveloped beaches, turquoise waters and colorful coral reefs! Feast your eyes on the amazing scenery, snorkel and get a glimpse of the thriving sea life!The boat trip includes stopover at some amazing places in Boracay where you can go snorkeling and swimming. Snorkeling gears will be provided for you.",
      "image_url":"https://cdn5.myboracayguide.com/2016/09/Private-Island-Hopping-Boracay-Activity-8-400x267.jpg",
      "price":"2900"
  },
  {
      "id":"8f086c95-df7d-4914-98b5-e3378663e967",
      "name":"Paraw Sailing",
      "description":"Paraw Sailing is a local sail boat\u00a0activity. The boats use two outriggers and two sails. Experience the traditional way of sailing and discover the best sites around the island, perfect for photography \u2013 though do note on days with heavier waves the water can kick up a bit (exciting!). If you schedule your activity for later in the afternoon you can take advantage of the incredible sunset while relaxing on the boat for half an hour. Sea sickness? usually not a problem as the boats tend to stay closer into the shore and cut through the waves very well. \u00a0Paraw sailing around Boracay is probably a really good way to ease yourself into the sea and find out how much you like it.",
      "image_url":"https://cdn5.myboracayguide.com/2016/03/Paraw-Sailing-Boracay-Activities-400x267.jpg",
      "price":"3000"
  },
  {
      "id":"6aa0ed0f-ddcc-42ff-8059-eea5ee40496d",
      "name":"Parasailing",
      "description":"Parasailing on Boracay is a great experience for a few adventure-minded individuals. Imagine being whisked into the sky while strapped in a seat covered by a colorful parachute! This is a popular activity where riders can view the beautiful shoreline of white beach from above while being pulled by a boat. This is a fun and exciting experience for those who love heights and want a birds-eye-view of the whole island. Up to two guests can occupy the same canopy.",
      "image_url":"https://cdn5.myboracayguide.com/2016/04/Parasailing-Boracay-Activities-400x267.jpg",
      "price":"2500"
  },
  {
      "id":"c5f7878a-70cd-49da-9a24-ca0b86beb71c",
      "name":"Boracay Pub Crawl",
      "description":"Boracay Pub Crawl is the biggest, hippest and most happening bar-hopping event on Boracay! Meet amazing people from around the world, play get to know you games to break the ice, drink welcome shooters with your free shooter glass, get discounts on drinks, free entrance in bars, and wear your iconic pub crawl shirt! This is definitely one of the most awesome ways to experience the island\u2019s famous nightlife and also a great chance to take pictures. Boracay PubCrawl is the first of its kind to offer both travelers and locals the chance to party as one big, wild group. Discover the best night spots and make new friends over the course of a great evening out.",
      "image_url":"https://cdn5.myboracayguide.com/2016/04/Boracay-Pub-Crawl-Activities-400x267.jpeg",
      "price":"990"
  },
  {
      "id":"0c3b6e63-9a92-4662-8a44-d3d9adc334c2",
      "name":"Sunset Party Cruise Booty",
      "description":"Aside from its amazing parties, Boracay is world famous for its breath-taking sunset. Hop on the island\u2019s 40 passenger party vessel, Booty, and jam with other travelers as you listen to great music! Definitely a memorable party at sundown!",
      "image_url":"https://cdn5.myboracayguide.com/2016/04/Sunset-Party-Cruise-Booty-400x267.jpg",
      "price":"2500"
  },
  {
      "id":"36b74f58-084d-4b67-9daa-a046296604e6",
      "name":"Ariels Point",
      "description":"Let us help you experience everything good about Ariel\u2019s Point. Many guests come for the 5 different levels of cliff diving; the cliff diving levels are generally suitable for all types of adventurers. Those that want a great photo in a naturally beautiful place\u00a0while having a bit of a jump, won\u2019t be disappointed or terrified. Similarly, hardcore guests that want to jump from the top of a volcanically hewn outcrop into the deep blue arms of the sea won\u2019t be let down either. \u00a0Ariel\u2019s Point is located near the rustic fishing town of Buruanga, a half hour boat ride from Boracay\u2019s white beach. Gather with other travelers as you snorkel, paddle in a native canoe, or just laze under the sun while enjoying the uniquely rough, &\u00a0comfortable environment.",
      "image_url":"https://cdn5.myboracayguide.com/2016/04/Ariels-Point-Boracay-Activities-1-400x267.jpg",
      "price":"2800"
  },
  {
      "id":"420cb55b-99cb-45b1-a860-d079cc1d2cea",
      "name":"Stand Up Paddle on the Beach",
      "description":"Experience how it\u2019s like to glide on the water surface from a Stand-Up Paddle Board. Paddling on a Stand-Up Paddle board for lets you commune with the current of the sea, either by standing up, kneeling or sitting down. It also provides a good exercise to maintain your balance and to strengthen your core, while you paddle into the water to workout your arms and upper body.",
      "image_url":"https://cdn5.myboracayguide.com/2016/10/Stand-Up-Paddle-Boracay-Activity-01-400x267.jpg",
      "price":"1000"
  },
  {
      "id":"778bad3e-6fb4-4deb-8ff2-120bcbc5f27e",
      "name":"Segway Tours",
      "description":"Surrender to the freedom of gliding along Boracay\u2019s scenic spots on a Segway. For an exhilarating hour, you will be able to feel a gratifying oneness with the Segway and surrender to its awesome mechanism, giving you a relaxed and confident exploration into the island\u2019s diverse sceneries. This eco-freindly joyride kicks off with a short video presentation at its booth inside the panoramic grounds of Fairways and Blue Water. A routine trial thence follows, and after, the actual Segway ride takes place. The first leg encompasses a comfortable descent on the pavement, where beginners",
      "image_url":"https://cdn5.myboracayguide.com/2016/08/Segway-Tours-Boracay-Activities-01-400x267.jpg",
      "price":"2300"
  },
  {
      "id":"7c72e357-7228-4b6c-bdd0-d9aab71512ac",
      "name":"Helicopter Beach Tour",
      "description":"Boracay Helicopter Beach Tour \u2013 It\u2019s never been better. Have a 10-minute adrenaline-filled experience of touring the island by helicopter! See Boracay\u2019s white sands, blue green waters, and reefs from above! This is the ultimate chance to snap birds-eye-view photographs!",
      "image_url":"https://cdn5.myboracayguide.com/2010/01/Boracay-Helicopter-Tours-Boracay-Activity-07-400x267.jpg",
      "price":"5200"
  }
]
```

### Step 1.7: Add product_routes.py
```bash
$ cd ~/environment/myproject-product-restapi
$ vi product_routes.py
```
```python
import os
import uuid
from flask import Blueprint
from flask import Flask, json, Response, request, abort
from custom_logger import setup_logger

# Set up the custom logger and the Blueprint
logger = setup_logger(__name__)
product_module = Blueprint('products', __name__)


logger.info("Intialized product routes")

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'products_boracay.json')

# load products static db from json file
with open(my_file) as f:
    products = json.load(f)


# Allow the default route to return a health check
@product_module.route('/')
def health_check():
    return "This a health check. Product Management Service is up and running."

    
@product_module.route('/products')
def get_all_products():
    
    try:
        serviceResponse = json.dumps({'products': products})
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    
    return resp
    
@product_module.route("/products/<string:product_id>", methods=['GET'])
def get_product(product_id):
    
    product = [p for p in products if p['id'] == product_id]

    try:
        serviceResponse = json.dumps({'products': product[0]})
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products", methods=['POST'])
def create_product():

    try:
        product_dict = json.loads(request.data)

        product = {
            'id': str(uuid.uuid4()),
            'name': product_dict['name'],
            'description': product_dict['description'],
            'image_url': product_dict['image_url']
        }

        products.append(product)

        serviceResponse = json.dumps({
                'products': product,
                'status': 'CREATED OK'
                })

        resp = Response(serviceResponse, status=201)

    except Exception as e:
        logger.error(e)
        abort(400)
   

    resp.headers["Content-Type"] = "application/json"

    return resp


@product_module.route("/products/<product_id>", methods=['PUT'])
def update_product(product_id):
    
    try:
        #creates a new product. The product id is automatically generated.
        product_dict = json.loads(request.data)
        
        product = [p for p in products if p['id'] == product_id]

        product[0]['name'] = request.json.get('name', product[0]['name'])
        product[0]['description'] = request.json.get('description', product[0]['description'])
        product[0]['image_url'] = request.json.get('image_url', product[0]['image_url'])
        
        product = {
            'name': request.json.get('name', product[0]['name']), 
            'description' : request.json.get('description', product[0]['description']),
            'image_url' : request.json.get('image_url', product[0]['image_url'])
        }

        serviceResponse = json.dumps({
                'products': product,
                'status': 'UPDATED OK'
                })

    except Exception as e:
        logger.error(e)
        abort(404)
   
    resp = Response(serviceResponse, status=200)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    try:
        product = [p for p in products if p['id'] == product_id]

        #deletes a product given its id.
        serviceResponse = json.dumps({
                'products' : product,
                'status': 'DELETED OK'
            })

        products.remove(product[0])

    except Exception as e:
        logger.error(e)
        abort(400)
   

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.errorhandler(404)
def item_not_found(e):
    # note that we set the 404 status explicitly
    return json.dumps({'error': 'Product not found'}), 404

@product_module.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return json.dumps({'error': 'Bad request'}), 400

```

### Step 1.8: Add app.py and custom_logger.py
- Add app.py
```bash
$ cd ~/environment/myproject-product-restapi
$ vi app.py
```
```python
from flask import Flask
from flask_cors import CORS

# Add new blueprints here
from product_routes import product_module

# Initialize the flask application
app = Flask(__name__)
CORS(app)

# Add a blueprint for the products module
app.register_blueprint(product_module)

# Run the application
app.run(host="0.0.0.0", port=5000, debug=True)
```

- custom_logger.py
```bash
$ cd ~/environment/myproject-product-restapi
$ vi custom_logger.py
```
```python
import logging

def setup_logger(name):
    formatter = logging.Formatter(fmt='[%(levelname)s][{}] %(asctime)s:%(threadName)s:%(message)s'.format(name), datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    return logger
```


### (TODO) Step 1.10: Backend Unit Tests

### Step 1.10: Generate requirements.txt


```bash
$ cd ~/environment/myproject-product-restapi
$ vi requirements.txt
```
```txt
Flask==1.0.2
flask-cors==3.0.7
```

Install the dependencies
```bash
$ pip install -r requirements.txt
```


### Step 1.11: Run Locally and Test
```bash
$ cd ~/environment/myproject-product-restapi
$ python app.py
$ curl http://localhost:5000
```


### Step 1.12: Create the Dockerfile
```bash
$ cd ~/environment/myproject-product-restapi 
$ vi Dockerfile
```
```
# Set base image to python
FROM python:3.7
ENV PYTHONBUFFERED 1

# Copy source file and python req's
COPY . /app
WORKDIR /app

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set image's main command and run the command within the container
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
```

### Step 1.13: Build, Tag and Run the Docker Image locally
Replace:
- AccountId: 707538076348 <--- get this from IAM user
- Region: ap-southeast-1

```bash
$ docker build -t <AccountId>.dkr.ecr.<Region>.amazonaws.com/myproject-product-restapi:latest .
$ docker run -p 5000:5000 myproject-product-restapi:latest
```

### Step 1.14: Test CRUD Operations
- Test Get all Products
```bash
curl -X GET \
  http://localhost:5000/products \
  -H 'Host: localhost:5000'
```
Response:
```json
{
    "products": [
        {
            "description": "Used to wash body",
            "image_url": "https://via.placeholder.com/150",
            "name": "Soap",
            "product_id": "4e53920c-505a-4a90-a694-b9300791f0ae"
        },
        {
            "description": "Used to wash hair",
            "image_url": "https://via.placeholder.com/150",
            "name": "Shampoo",
            "product_id": "2b473002-36f8-4b87-954e-9a377e0ccbec"
        },
        {
            "description": "thin, soft paper, typically used for wrapping or protecting fragile or delicate articles.",
            "image_url": "https://via.placeholder.com/150",
            "name": "Tissue",
            "product_id": "3f0f196c-4a7b-43af-9e29-6522a715342d"
        }
    ]
}
```

- Test Get Product
```bash
curl -X GET \
  http://localhost:5000/products/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Host: localhost:5000' 
```

Response: 
```bash
{
    "products": {
        "description": "Used to wash body",
        "image_url": "https://via.placeholder.com/150",
        "name": "Soap",
        "product_id": "4e53920c-505a-4a90-a694-b9300791f0ae"
    }
}
```

- Test Create Product
```bash
curl -X POST \
  http://localhost:5000/products \
  -H 'Content-Type: application/json' \
  -d '{
  "name":"Product G",
  "description": "Nulla nec dolor a ipsum viverra tincidunt eleifend id orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.",
  "image_url": "https://via.placeholder.com/200",
}'
```

Response
```json
{
    "products": {
        "description": "Nulla nec dolor a ipsum viverra tincidunt eleifend id orci. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.",
        "image_url": "https://via.placeholder.com/200",
        "name": "Product G",
        "product_id": "83b2376e-955c-4f8e-96d5-95a5549ddf2d"
    },
    "status": "CREATED OK"
}
```



- Test Update Product
```bash
curl -X PUT \
  http://localhost:5000/products/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json' \
  -d '{
  "name":"egg 123",
  "description": "my working description dasdasds",
  "image_url": "product_image testes update test"
}'
```


Response
```json
{
    "products": {
        "description": "my working description dasdasds",
        "image_url": "product_image testes update test",
        "name": "egg 123"
    },
    "status": "UPDATED OK"
}
```


- Test Delete Product
```bash
curl -X DELETE \
  http://localhost:5000/products/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json' 
```

Response
```json
{
    "products": [
        {
            "description": "my working description dasdasds",
            "image_url": "product_image testes update test",
            "name": "egg 123",
            "product_id": "4e53920c-505a-4a90-a694-b9300791f0ae"
        }
    ],
    "status": "DELETED OK"
}
```


### Step 1.15: Push to Remote Repository
```bash
$ cd ~/environment/myproject-product-restapi
$ git add .
$ git commit -m "Initial Commit"
$ git push origin master
```

### Step 1.16: Create the ECR Repository
```bash
$ aws ecr create-repository --repository-name myproject-product-restapi
```

### Step 1.17: Run login command to retrieve credentials for our Docker client and then automatically execute it (include the full command including the $ below).
```bash
$ $(aws ecr get-login --no-include-email)
```

### Step 1.18: Push our Docker Image

Replace:
- AccountId: 707538076348 <--- get this from IAM user
- Region: us-east-1

```bash
$ docker push <AccountId>.dkr.ecr.<Region>.amazonaws.com/myproject-product-restapi:latest
```

### Step 1.19: Validate Image has been pushed
```bash
$ aws ecr describe-images --repository-name myproject-product-restapi
```

### (Optional) Clean up
```bash
$ aws ecr delete-repository --repository-name myproject-product-restapi --force
$ aws codecommit delete-repository --repository-name myproject-product-restapi
$ rm -rf ~/environment/myproject-product-restapi
```
