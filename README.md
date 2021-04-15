# POC - Recomender

Proof of concept for a recommendation system of products based on the Flipkart Products dataset.

Recommendations are made based on product name and product description, using cosine distance between sentence embeddings.

## Request & Response Examples

### API Resources

  - [GET /](#get-)
  - [POST /recommend](#post-recommend)
  

### GET /

Example: http://localhost:5000/

Description: Response with a welcome message.   

Response body:

    {
        'message': "Hello! This is the recommender system"
    }
    
### POST /recommend

Example: Create – POST  http://localhost:5000/recommend

Description: Gives K recommendations similar to *uniq_id*.

Request body:

    {
        'uniq_id': "f465dfcbf48cb1e4cde0f5cd1da50aac",
    }
    
(200) Response body:

    {
        'values': [
                *product_entry_1*,
                *product_entry_2*,
                *product_entry_3*,
        ],
        'scores': [0.92, 0.92, 0.87]
    }


(404) Response body:

    {
        'message': 'Unable to retrieve item *definetly_not_a_uniq_id*'
    }


## Description of components

* **app.py** : Flask app as REST API.

* **README.md** : [This](https://github.com/ramonzaca/poc_recommender).

* **requirements.txt** : PIP requirements for the docker.

* **Dockerfile** : Description of the docker.

* **recommender.py** : Recommendation system code.

* **Dockerfile** : Description of the docker.

* **config.py** : Configuration file.

## Usage

Starting from the repo folder.

* Building the image: ```docker build -t recommender:latest .```.
* Run the image: ```docker run -p 5000:5000 recommender```.

*Notes:* 

- *The system can also be start locally via **python app.py**, if all requirements are installed.*


