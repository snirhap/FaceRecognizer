from faker import Faker
from numpy import dot, linalg, random
from flask import Flask, request, jsonify
from flask_api import status
from db import MongoDBHandler


DESIRED_TOP_MATCHES = 3
NUM_OF_FEATURES = 256
PROXIMATE = 5
DB_NAME = "DB"
PERSONS_COLLECTION_NAME = "persons"
MAX_PERSONS_IN_COLLECTION = 200

# NUM_OF_FEATURES = 256

app = Flask(__name__)
db_handler = MongoDBHandler(DB_NAME)


def vector_generator():
    return [round(feature, PROXIMATE) for feature in random.rand(NUM_OF_FEATURES).tolist()]


# def normalize_vector(vector_to_normalize):
#     return (vector_to_normalize / linalg.norm(vector_to_normalize, axis=-1, ord=2)).tolist()


def get_top_matches(compare):
    return sorted(compare, key=lambda k: k['result'], reverse=True)


@app.route('/', methods=['GET'])
def face_recognition():
    compare = []
    input_data = request.get_json()
    if input_data:
        message, status_code = get_person_input_validation(input_data)
        if status_code == status.HTTP_200_OK:
            features = request.get_json()["features"]
            for person in db_handler.scan_collection(PERSONS_COLLECTION_NAME):
                dot_prod = dot(features, person["features"])
                # Cosine similarity
                cos_sim = round(dot_prod / (linalg.norm(features) * linalg.norm(person["features"])), PROXIMATE)
                compare.append({"person_name": person["person_name"], "result": cos_sim})
            top_matches = get_top_matches(compare)
            return jsonify(top_matches[:DESIRED_TOP_MATCHES])
        else:
            return f'Invalid input, {message}', status.HTTP_400_BAD_REQUEST
    else:
        return jsonify(db_handler.scan_collection(PERSONS_COLLECTION_NAME))


@app.route('/add', methods=['POST'])
def add_one_person():
    input_data = request.get_json()
    if db_handler.count_documents_in_collection(PERSONS_COLLECTION_NAME) > MAX_PERSONS_IN_COLLECTION:
        return f'persons collection has reached its maximum capacity of {MAX_PERSONS_IN_COLLECTION} records', \
               status.HTTP_500_INTERNAL_SERVER_ERROR

    message, status_code = add_person_input_validation(input_data)

    if status_code == status.HTTP_200_OK:
        # Check duplicate records
        # ...

        db_handler.insert_one_to_collection(PERSONS_COLLECTION_NAME,
                                            {"person_name": input_data.get('person_name'),
                                             "features": [round(feature, PROXIMATE) for feature in input_data.get('features')]})
        return f"{status_code}: {input_data.get('person_name')} was added to DB", status.HTTP_201_CREATED
    else:
        return f"{status_code}: could not add to DB - {message}", status_code


def get_person_input_validation(input_data):
    error_message = ''
    if input_data.get('features') is None or not isinstance(input_data.get('features'), list) or not \
            all(isinstance(feature, (int, float)) for feature in input_data.get('features')):
        error_message = 'features list is empty or some features are not float numbers'
    elif len(input_data.get('features')) != NUM_OF_FEATURES:
        error_message = f'input vector number of features should be {NUM_OF_FEATURES}'

    if error_message:
        return error_message, status.HTTP_400_BAD_REQUEST
    return "OK", status.HTTP_200_OK


def add_person_input_validation(input_data):
    error_message = ''
    if not input_data:
        error_message = 'input is empty'
    elif input_data.get('person_name') is None or not isinstance(input_data.get('person_name'), str):
        error_message = 'person name is empty or not a string'
    elif input_data.get('features') is None or not isinstance(input_data.get('features'), list) or not \
            all(isinstance(feature, (int, float)) for feature in input_data.get('features')):
        error_message = 'features list is empty or some features are not float numbers'
    elif len(input_data.get('features')) != NUM_OF_FEATURES:
        error_message = f'input vector number of features should be {NUM_OF_FEATURES}'

    if error_message:
        return error_message, status.HTTP_400_BAD_REQUEST
    return "OK", status.HTTP_200_OK


def fill_db():
    fake = Faker()
    fake_persons = [{"person_name": fake.name(), "features": vector_generator()} for _ in range(100)]
    db_handler.get_collection(PERSONS_COLLECTION_NAME).insert_many(fake_persons)


if __name__ == '__main__':
    # fill_db()
    # db_handler.truncate_collection(PERSONS_COLLECTION_NAME)
    # fill_db()
    app.run(debug=True)
