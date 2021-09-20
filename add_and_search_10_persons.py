import requests
from faker import Faker
from numpy import random

from modules import config

IP = "0.0.0.0:5000"
NUMBER_OF_RECORDS = 10
fake = Faker()


def vector_generator():
    return [round(feature, config.FEATURE_PROXIMITY) for feature in random.rand(config.NUMBER_OF_FEATURES).tolist()]


def create_and_search():
    generated_persons = [{config.PERSON_NAME_COLUMN: fake.name(),
                          config.FEATURES_COLUMN: vector_generator()} for _ in range(NUMBER_OF_RECORDS)]

    for person in generated_persons:
        response = requests.post(url=f'http://{IP}/add_person', json=person)
        print(response.content)

    for person in generated_persons:
        response = requests.get(url=f'http://{IP}/', json={config.FEATURES_COLUMN: person[config.FEATURES_COLUMN]}).json()
        print(f'Best matches for {person[config.PERSON_NAME_COLUMN]}:\n{response}')


if __name__ == '__main__':
    create_and_search()
