from modules import config


def add_person_input_validation(input_data: dict):
    person_name = input_data[config.PERSON_NAME_COLUMN]
    features = input_data[config.FEATURES_COLUMN]
    if not input_data:
        raise ValueError('input is empty')
    elif not isinstance(person_name, str):
        raise ValueError('person name is not a string')
    elif not isinstance(features, list) or not all(isinstance(feature, (int, float)) for feature in features):
        raise ValueError('features list is empty or some features are not float numbers')
    elif len(input_data.get(config.FEATURES_COLUMN)) != config.NUMBER_OF_FEATURES:
        raise ValueError(f'input vector number of features should be {config.NUMBER_OF_FEATURES}')


def get_person_input_validation(input_data: dict):
    features = input_data[config.FEATURES_COLUMN]
    if not isinstance(features, list) or not \
            all(isinstance(feature, (int, float)) for feature in features):
        raise ValueError('features list is empty or some features are not float numbers')
    elif len(features) != config.NUMBER_OF_FEATURES:
        raise ValueError(f'input vector number of features should be {config.NUMBER_OF_FEATURES}')
