from faker import Faker
from flask.json import dumps
from numpy import dot, linalg, random
from flask import Flask, request, jsonify, Response
from flask_mongoengine import MongoEngine
from flask_api import status

app = Flask(__name__)
db = MongoEngine()
db.init_app(app)

DESIRED_TOP_MATCHES = 3
NUM_OF_FEATURES = 5
PROXIMATE = 5
# NUM_OF_FEATURES = 256


def vector_generator():
    return [round(feature, PROXIMATE) for feature in random.rand(NUM_OF_FEATURES).tolist()]


# def normalize_vector(vector_to_normalize):
#     return (vector_to_normalize / linalg.norm(vector_to_normalize, axis=-1, ord=2)).tolist()


def get_top_matches(compare):
    return sorted(compare, key=lambda k: k['result'], reverse=True)


@app.route('/', methods=['POST', 'GET'])
def face_recognition():
    # if request.method == 'POST':
    #     content = request.get_json()
    #     if content.get('person_name', None) and content.get('features'):
    #         db_list.append({"person_name": content.get('person_name'),
    #                         "features": content.get('features')})
    #                         # "features": normalize_vector(content.get('features'))})
    #         return f"{content.get('person_name')} was added to DB"
    #     else:
    #         return f"Input data is missing parameters"
    # elif request.method == 'GET':
    compare = []
    content = request.get_json()
    if content:
        features = request.get_json()["features"]
        # features = normalize_vector(request.get_json()["features"])
        for person in db_list:
            dot_prod = dot(features, person["features"])
            # Cosine similarity
            cos_sim = dot_prod / (linalg.norm(features) * linalg.norm(person["features"]))
            print(f'name: {person["person_name"]}; cos_sim: {cos_sim}')
            compare.append({"person_name": person["person_name"], "result": cos_sim})
        top_matches = get_top_matches(compare)
        return jsonify(top_matches[:DESIRED_TOP_MATCHES])
    else:
        return jsonify(db_list)


def add_person_input_validation(content):
    error_message = ''
    print(content)
    if not content:
        error_message = 'Input is empty'
    elif content.get('person_name') is None or not isinstance(content.get('person_name'), str):
        error_message = 'Person name is empty or not a string'
    elif content.get('features') is None or not isinstance(content.get('features'), list) or not \
            all(isinstance(feature, (int, float)) for feature in content.get('features')):
        error_message = 'Features list is empty or some features are not float numbers'
    elif len(content.get('features')) != NUM_OF_FEATURES:
        error_message = f'Input vector number of features should be {NUM_OF_FEATURES}'

    if error_message:
        return error_message, status.HTTP_400_BAD_REQUEST
    return "OK", status.HTTP_200_OK


@app.route('/add', methods=['POST'])
def add_one_person():
    content = request.get_json()
    message, status_code = add_person_input_validation(content)

    if status_code == status.HTTP_200_OK:
        db_list.append({"person_name": content.get('person_name'),
                        "features": [round(feature, PROXIMATE) for feature in content.get('features')]})
        # "features": normalize_vector(content.get('features'))})
        return f"{status_code}: {content.get('person_name')} was added to DB"
    else:
        return f"{status_code}: Could not add to DB - {message}"


def fill_db_list():
    fake = Faker()
    return [{"person_name": fake.name(), "features": vector_generator()} for _ in range(10)]
    # return [{"person_name": fake.name(), "features": normalize_vector(vector_generator())} for _ in range(100)]


if __name__ == '__main__':
    db_list = fill_db_list()
    app.run(debug=True)
