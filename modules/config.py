import json


def get_config_file():
    with open('./resources/config.json', 'r') as config_file:
        config = json.load(config_file)
    return config


config = get_config_file()
FEATURE_PROXIMITY = config['feature_proximity']
DESIRED_TOP_MATCHES = config['desired_top_matches']
NUMBER_OF_FEATURES = config['number_of_features']
NUMBER_OF_THREADS = config['number_of_threads']
MAX_RECORDS_IN_COLLECTION = config['max_records_in_collection']
MAX_RECORDS_THRESHOLD_WARNING = config['max_records_threshold_warning']
PERSONS_COLLECTION_NAME = config['persons_collection_name']
DB_NAME = config['db_name']
SERVER_IP = config['ip']
SERVER_PORT = config['port']
PERSON_NAME_COLUMN = config['person_name_column']
FEATURES_COLUMN = config['person_features_column']
RESULT_FIELD = config['result_field']
