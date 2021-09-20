from flask import Flask, request, jsonify
from flask_api import status

import config
import logics
import validation
from exceptions import DuplicateDocument, MaximumDocumentsInCollection

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_closest_match():
    try:
        input_data = request.json
        validation.get_person_input_validation(input_data)
        features = input_data[config.FEATURES_COLUMN]
        top_matches = logics.get_most_similar_persons(features)
        return jsonify(top_matches), status.HTTP_200_OK
    except KeyError as error:
        return f'Missing key: {error}', status.HTTP_400_BAD_REQUEST
    except ValueError as error:
        return f'Invalid input: {error}', status.HTTP_400_BAD_REQUEST
    except Exception as error:
        return f'Error: {error}', status.HTTP_400_BAD_REQUEST


@app.route('/add_person', methods=['POST'])
def add_one_person():
    try:
        input_data = request.json
        validation.add_person_input_validation(input_data)
        logics.insert_document_to_persons_collection(input_data=input_data)
        return f'{input_data.get(config.PERSON_NAME_COLUMN)} was added to {config.PERSONS_COLLECTION_NAME}', status.HTTP_201_CREATED
    except DuplicateDocument as error:
        return f'Error adding new person: {error}', status.HTTP_400_BAD_REQUEST
    except MaximumDocumentsInCollection as error:
        return f'Error adding new person: {error}', status.HTTP_400_BAD_REQUEST
    except KeyError as error:
        return f'Missing key {error}', status.HTTP_400_BAD_REQUEST
    except ValueError as error:
        return f'Invalid input: {error}', status.HTTP_400_BAD_REQUEST
    except Exception as error:
        return f'Error adding new person. {error}', status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=config.PORT)
