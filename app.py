from queue import Queue
from threading import Thread
from faker import Faker
from numpy import dot, linalg, random
from flask import Flask, request, jsonify
from flask_api import status
from db import MongoDBHandler
from json import load


def get_config_file():
    with open('resources/config.json', 'r') as config_file:
        config = load(config_file)
    return config


configs = get_config_file()
app = Flask(__name__)
db_handler = MongoDBHandler(configs["db_name"])


@app.route('/', methods=['GET'])
def get_closest_match():
    input_data = request.get_json()
    if input_data:
        message, status_code = get_person_input_validation(input_data)
        if status_code == status.HTTP_200_OK:
            features = request.get_json()["features"]
            top_matches = get_most_similar_persons(features, list(db_handler.find_in_collection(configs["persons_collection_name"])))
            return jsonify(top_matches)
        else:
            return f'Invalid input, {message}', status.HTTP_400_BAD_REQUEST


def get_most_similar_persons(query_vector: list, collection_vectors: list):
    workers = list()
    processed_results = list()
    queue_to_process = Queue()

    # Fill queue with all persons
    for element in collection_vectors:
        queue_to_process.put(element)

    for i in range(configs["number_of_threads"]):
        worker = Thread(target=process_queue_elements, args=(queue_to_process, query_vector, processed_results))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    return get_top_matches(processed_results)


def process_queue_elements(queue_to_process: Queue, query_vector: list, processed_results: list):
    while not queue_to_process.empty():
        queue_vector = queue_to_process.get()
        processed_results.append(get_similarity_for_query_vector(query_vector, queue_vector))


def get_similarity_for_query_vector(query_vector: list, queue_vector: dict):
    return {"person_name": queue_vector["person_name"],
            "result": get_features_similarity_between_two_vectors(query_vector, queue_vector["features"])}


def get_features_similarity_between_two_vectors(first_vector: list, second_vector: list):
    # Calculate cosine similarity between 2 features vector
    dot_prod = dot(first_vector, second_vector)
    return round(dot_prod / (linalg.norm(first_vector) * linalg.norm(second_vector)), configs["feature_proximity"])


@app.route('/add', methods=['POST'])
def add_one_person():
    input_data = request.get_json()
    if db_handler.count_documents_in_collection(configs["persons_collection_name"]) > configs["max_records_in_collection"]:
        return f'persons collection has reached its maximum capacity of {configs["max_records_in_collection"]} records', \
               status.HTTP_500_INTERNAL_SERVER_ERROR

    message, status_code = add_person_input_validation(input_data)
    if status_code == status.HTTP_200_OK:
        db_handler.insert_one_to_collection(configs["persons_collection_name"],
                                            {"person_name": input_data.get('person_name'),
                                             "features": [round(feature, configs["feature_proximity"]) for feature in input_data.get('features')]})
        return f"{status_code}: {input_data.get('person_name')} was added to DB", status.HTTP_201_CREATED
    else:
        return f"{status_code}: could not add to DB - {message}", status_code


def get_person_input_validation(input_data):
    error_message = ''
    if input_data.get('features') is None or not isinstance(input_data.get('features'), list) or not \
            all(isinstance(feature, (int, float)) for feature in input_data.get('features')):
        error_message = 'features list is empty or some features are not float numbers'
    elif len(input_data.get('features')) != configs["number_of_features"]:
        error_message = f'input vector number of features should be {configs["number_of_features"]}'

    if error_message:
        return error_message, status.HTTP_400_BAD_REQUEST
    return "OK", status.HTTP_200_OK


def is_person_already_exists(person_name: str):
    return db_handler.count_documents_in_collection(configs["persons_collection_name"], {"person_name": person_name})


def add_person_input_validation(input_data):
    error_message = ''
    if not input_data:
        error_message = 'input is empty'
    elif input_data.get('person_name') is None or not isinstance(input_data.get('person_name'), str):
        error_message = 'person name is empty or not a string'
    elif input_data.get('features') is None or not isinstance(input_data.get('features'), list) or not \
            all(isinstance(feature, (int, float)) for feature in input_data.get('features')):
        error_message = 'features list is empty or some features are not float numbers'
    elif len(input_data.get('features')) != configs["number_of_features"]:
        error_message = f'input vector number of features should be {configs["number_of_features"]}'
    elif is_person_already_exists(input_data.get('person_name')):
        error_message = f'{input_data.get("person_name")} already exists'
    if error_message:
        return error_message, status.HTTP_400_BAD_REQUEST
    return "OK", status.HTTP_200_OK


def get_top_matches(compare):
    return sorted(compare, key=lambda k: k['result'], reverse=True)[:configs["desired_top_matches"]]


# def fill_db(self, collection_name: str, number_of_records: int):
#     fake = Faker()
#     fake_persons = [{"person_name": fake.name(), "features": self.vector_generator()} for _ in range(number_of_records)]
#     print(fake_persons)
#     # self.db_handler.get_collection(collection_name).insert_many(fake_persons)
#
#
# def vector_generator():
#     return [round(feature, configs.get("feature_proximity")) for feature in random.rand(configs.get("number_of_features")).tolist()]


if __name__ == '__main__':
    # db_handler.truncate_collection(configs["persons_collection_name"])
    # db_filler = DbFiller(db_handler)
    # db_filler.fill_db()
    app.run(debug=True)
