import time
from queue import Queue
from threading import Thread
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
NUM_OF_THREADS = 3
MAX_PERSONS_IN_COLLECTION = 10000

app = Flask(__name__)
db_handler = MongoDBHandler(DB_NAME)


def vector_generator():
    return [round(feature, PROXIMATE) for feature in random.rand(NUM_OF_FEATURES).tolist()]


def get_top_matches(compare):
    return sorted(compare, key=lambda k: k['result'], reverse=True)[:DESIRED_TOP_MATCHES]


@app.route('/', methods=['GET'])
def get_closest_match():
    input_data = request.get_json()
    if input_data:
        message, status_code = get_person_input_validation(input_data)
        if status_code == status.HTTP_200_OK:
            features = request.get_json()["features"]
            all_persons_in_collection = db_handler.scan_collection(PERSONS_COLLECTION_NAME)
            # Parallel best matches
            start = time.time()
            top_matches = get_similarity_multi_threaded(features, all_persons_in_collection)
            end = time.time()
            print(f"Runtime Multi Thread: {end - start}")
            print(f"Top Matches Multi Thread: {top_matches}")

            # # single thread
            # start = time.time()
            # top_matches = get_similarities_for_query_vector(features, all_persons_in_collection)
            # end = time.time()
            # print(f"Runtime Single Thread: {end - start}")
            # print(f"Top Matches Single Thread: {top_matches}")
            return jsonify(top_matches)
        else:
            return f'Invalid input, {message}', status.HTTP_400_BAD_REQUEST
    else:
        return jsonify(db_handler.scan_collection(PERSONS_COLLECTION_NAME))


def get_similarity_multi_threaded(query_vector: list, collection_vectors: list):
    workers = []
    processed_results = []
    queue_to_process = Queue()

    # Fill queue with all persons
    for element in collection_vectors:
        queue_to_process.put(element)

    for i in range(NUM_OF_THREADS):
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
    return round(dot_prod / (linalg.norm(first_vector) * linalg.norm(second_vector)), PROXIMATE)


# Single thread
def get_similarities_for_query_vector(query_vector: list, collection_vectors: list):
    compare = []
    for person in collection_vectors:
        compare.append({"person_name": person["person_name"],
                        "result": get_features_similarity_between_two_vectors(query_vector, person["features"])})
    return get_top_matches(compare)

# def get_similarity_multi_threaded(query_vector: list, collection_vectors: list):
#     threads = []
#     threads_results = []
#     number_of_threads = 5
#     with ThreadPoolContext(number_of_threads) as tp_ctx:
#         chunk_size = db_handler.count_documents_in_collection(PERSONS_COLLECTION_NAME) // number_of_threads
#         for chunk in divide_list_into_chunks(collection_vectors, chunk_size):
#             threads.append(tp_ctx.apply_async(get_similarities_for_query_vector, (query_vector, chunk,)))
#
#     for thread in threads:
#         threads_results.extend(thread.get())
#
#     return get_top_matches(threads_results)
    # threads_results = []
    # with futures.ThreadPoolExecutor() as executor:
    #     # fixme 10
    #     chunk_size = db_handler.count_documents_in_collection(PERSONS_COLLECTION_NAME) // 10
    #     for chunk in divide_list_into_chunks(collection_vectors, chunk_size):
    #         future = executor.submit(get_similarities_for_query_vector, query_vector, chunk)
    #         threads_results.extend(future.result())
    # return get_top_matches(threads_results)


def divide_list_into_chunks(vector: list, number_of_chunks: int):
    for i in range(0, len(vector), number_of_chunks):
        yield vector[i: i + number_of_chunks]


@app.route('/add', methods=['POST'])
def add_one_person():
    input_data = request.get_json()
    if db_handler.count_documents_in_collection(PERSONS_COLLECTION_NAME) > MAX_PERSONS_IN_COLLECTION:
        return f'persons collection has reached its maximum capacity of {MAX_PERSONS_IN_COLLECTION} records', \
               status.HTTP_500_INTERNAL_SERVER_ERROR

    message, status_code = add_person_input_validation(input_data)

    if status_code == status.HTTP_200_OK:
        # Check duplicate records?
        # db_handler.get_collection(PERSONS_COLLECTION_NAME).aggregate()

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
    fake_persons = [{"person_name": fake.name(), "features": vector_generator()} for _ in range(5000)]
    db_handler.get_collection(PERSONS_COLLECTION_NAME).insert_many(fake_persons)


if __name__ == '__main__':
    # db_handler.truncate_collection(PERSONS_COLLECTION_NAME)
    # fill_db()
    app.run(debug=True)
