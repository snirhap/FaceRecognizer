import requests
from faker import Faker
from numpy import random

from modules import config

IP = f'{config.SERVER_IP}:{config.SERVER_PORT}'
NUMBER_OF_RECORDS = 10
fake = Faker()


def vector_generator():
    return [round(feature, config.FEATURE_PROXIMITY) for feature in random.rand(config.NUMBER_OF_FEATURES).tolist()]


def add_persons():
    generated_persons = [{config.PERSON_NAME_COLUMN: fake.name(),
                          config.FEATURES_COLUMN: vector_generator()} for _ in range(NUMBER_OF_RECORDS)]

    for person in generated_persons:
        response = requests.post(url=f'http://{IP}/add_person', json=person)
        print(response.content)


if __name__ == '__main__':
    add_persons()
