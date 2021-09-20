from logging import getLogger
from queue import Queue
from threading import Thread

from numpy import dot, linalg

import config
from db import MongoDBHandler
from exceptions import DuplicateDocument, MaximumDocumentsInCollection

logger = getLogger(__name__)
db_handler = MongoDBHandler(config.DB_NAME)


def get_most_similar_persons(query_vector: list):
    workers = list()
    processed_results = list()
    queue_to_process = Queue()

    # Fill queue with all persons
    for element in db_handler.find_in_collection(config.PERSONS_COLLECTION_NAME):
        queue_to_process.put(element)

    for i in range(config.NUMBER_OF_THREADS):
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
    return {config.PERSON_NAME_COLUMN: queue_vector[config.PERSON_NAME_COLUMN],
            config.RESULT_FIELD: get_features_similarity_between_two_vectors(query_vector, queue_vector[config.FEATURES_COLUMN])}


def get_features_similarity_between_two_vectors(first_vector: list, second_vector: list):
    # Calculate cosine similarity between 2 features vector
    dot_prod = dot(first_vector, second_vector)
    return round(dot_prod / (linalg.norm(first_vector) * linalg.norm(second_vector)), config.FEATURE_PROXIMITY)


def is_person_already_exists(person_name: str):
    if db_handler.count_documents_in_collection(config.PERSONS_COLLECTION_NAME, {config.PERSON_NAME_COLUMN: person_name}) > 0:
        raise DuplicateDocument(f'{person_name} already in {config.PERSONS_COLLECTION_NAME}')


def has_collection_exceeded_maximum_documents(collection_name: str):
    if db_handler.count_documents_in_collection(collection_name) >= config.MAX_RECORDS_IN_COLLECTION:
        raise MaximumDocumentsInCollection(f'{collection_name} collection has reached its maximum capacity ({config.MAX_RECORDS_IN_COLLECTION})'
                                           f'{config.MAX_RECORDS_IN_COLLECTION} records')


def insert_document_to_persons_collection(input_data: dict):
    person_name = input_data[config.PERSON_NAME_COLUMN]
    person_features = input_data[config.FEATURES_COLUMN]
    is_person_already_exists(person_name=person_name)
    has_collection_exceeded_maximum_documents(collection_name=config.PERSONS_COLLECTION_NAME)
    db_handler.insert_one_to_collection(config.PERSONS_COLLECTION_NAME,
                                        {config.PERSON_NAME_COLUMN: person_name,
                                         config.FEATURES_COLUMN: [round(feature, config.FEATURE_PROXIMITY) for feature in person_features]})


def get_top_matches(compare):
    return sorted(compare, key=lambda k: k[config.RESULT_FIELD], reverse=True)[:config.DESIRED_TOP_MATCHES]

