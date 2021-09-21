# Face Recognizer Exrecise

Service that mimic a face recognition system.

Given a vector that contains features (256 elements/features) of face where each feature is represented by real number from 0 to 1, 
the service returns top 3 most similiar matches to this given vector.

The service exposes a Rest server which contains these APIs:

1. GET (```/```)
Must contain JSON as an input with a feature vector with 256 features, and in response, returns the top 3 most similiar persons to the input vector.

2. POST (```/add_person```)
Request's body must contain a person name and a vector of features, and adds it to persons "table".


Database that is used for this project is MongoDB's cloud service.


## Installation and Execution

### Locally
1. Clone repository's code, withing project directory, install all requirements via:
```
$ pip3 install -r requirements.txt
```

2. Setup enviroment variable for MongoDB's connection string
```
$ export MONGO_CONNECTION_STRING=<<DB_CONNECTION_STRING>>
```

3. Run main script (app.py) in terminal:
```
$ python app.py
```

### Via Docker Container
1. If using docker hub (https://hub.docker.com/r/snirhap92/facerecognition)

1.1. Pull the image from DockerHub: 
```
$ docker pull snirhap92/facerecognition
```

1.2. Run:
```
$ docker run -e MONGO_CONNECTION_STRING=<<DB_CONNECTION_STRING>> -e LOG_LEVEL_PARAMETER='INFO' -p 5000:5000 snirhap92/facerecognition
```

2.1. If using local build, under project folder, run:
```
$ docker build -t facerecognition:latest .
```

2.2. Run:
```
$ docker run -it -e MONGO_CONNECTION_STRING=<<DB_CONNECTION_STRING>> -e LOG_LEVEL_PARAMETER='INFO' -p 5000:5000 facerecognition
```

## Notes

1. There is an input validation for all requests. The server handles many exceptions related to the input that being given by the user,
and notifies the user wether a request was successful or not with appropriate message.
All validations implementation are located in modules/validation.py

2. User scripts
There are 2 scripts which simulate requests of POST and GET to the server:
+ add_10_persons.py - genearates data for 10 persons (name and features vector) and adds them to persons collection in the DB.
+ add_and_search_10_persons.py - adds 10 persons to persons collection and then search for each of one of them their closest matches.

You can run them when server is up using:
```
$ python add_10_persons.py
$ python add_and_search_10_persons.py
```

3. Logger
There is a logger (used in logics.py) that can be defined to work in all classic log levels using an environment variable (DEBUG, INFO, etc.) and can also be defined to be written to an output file.
