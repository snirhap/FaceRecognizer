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

Once the server is up, you may use curl command or Postman or user scripts to send requests to the server (using ```http://127.0.0.1:5000``` url)

## Examples:
### POST
```
curl -X POST -H "Content-type: application/json" -H "Accept: application/json" -d '{"person_name": "Chen Amiel", "features":[0.4142, 0.5, 0.12026, 0.70302, 0.5555, 0.7325, 0.6666, 0.82763, 0.97791, 0.86722, 0.01655, 0.43817, 0.69767, 0.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.06782, 0.82654, 0.12942, 0.17726, 0.11326, 0.17282, 0.00038, 0.81088, 0.9816, 0.40945, 0.74331, 0.80034, 0.71325, 0.91449, 0.12842, 0.29639, 0.93443, 0.70015, 0.47373, 0.48878, 0.75053, 0.52359, 0.29784, 0.39894, 0.56431, 0.85548, 0.79251, 0.1631, 0.38654, 0.50632, 0.26896, 0.34458, 0.21217, 0.6246234234, 0.24252, 0.06612, 0.49736, 0.32115, 0.05175, 0.74311, 0.46243, 0.46945, 0.8904, 0.52333, 0.3, 0.3, 0.3, 0.3, 0.90865, 0.67153, 0.01126, 0.97171, 0.87841, 0.49106, 0.13053, 0.17982, 0.82662,0.54264, 0.15469, 0.55414, 0.91683, 0.51145, 0.41477, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.58764, 0.88313, 0.37205, 0.02449, 0.52112, 0.87728, 0.777, 0.55553, 0.66, 0.02313, 0.11111, 0.80667, 0.53751, 0.0131, 0.65933, 0.18781, 0.74947, 0.96709, 0.80491, 0.6905, 0.9895, 0.04426, 0.39591, 0.42531, 0.30839, 0.56514, 0.63484, 0.7866, 0.68256, 0.10216, 0.48288, 0.35511, 0.60479, 0.11373, 0.24926, 0.7167, 0.42896, 0.17249, 0.53224, 0.65764, 0.37756, 0.8888, 0.1, 0.1, 0.1, 0.3539, 0.88888, 0.24885, 0.76737, 0.16757, 0.78549, 0.41, 0.1, 0.1, 0.1, 0.32993, 0.67534, 0.71187, 0.43277, 0.8, 0.666, 0.13769, 0.92555453, 0.82044, 0.911, 0.87363, 0.39582, 0.10465, 0.8, 0.7, 0.58114, 0.6, 0.2, 0.2, 0.3, 0.2, 0.1, 0.3, 0.8, 0.7, 0.6, 0.5, 0.4, 0.28247, 0.86139, 0.56019, 0.50764, 0.77718, 0.85172, 0.41824, 0.25684, 0.5, 0.4, 0.3, 0.55297, 0.8503, 0.30904, 0.99926, 0.85589, 0.444, 0.01316, 0.09911, 0.555, 0.87012, 0.41096, 0.48637, 0.85519, 0.47088, 0.1011, 0.25033, 0.09467, 0.40198, 0.96851, 0.82213, 0.12503, 0.20571, 0.25076, 0.06231, 0.07601, 0.45708, 0.11272, 0.63568, 0.23461, 0.34695, 0.09066, 0.43258, 0.8, 0.8, 0.8, 0.81373, 0.80286, 0.96214, 0.88751, 0.1231, 0.18324, 0.65326, 0.15867, 0.38488, 0.65268, 0.32696, 0.94382, 0.53507, 0.76713, 0.14548, 0.48512, 0.9634, 0.06756, 0.072, 0.39152, 0.31019, 0.6, 0.7, 0.49246, 0.228802, 0.08583, 0.03398, 0.0285, 0.5462, 0.24258, 0.14214, 0.07815, 0.4124, 0.123, 0.93681, 0.57008, 0.31158]}' "http://127.0.0.1:5000/add_person"
```

### GET
```
$ curl -X GET -H "Content-type: application/json" -H "Accept: application/json" -d '{"features":[0.4142, 0.5, 0.12026, 0.70302, 0.5555, 0.7325, 0.6666, 0.82763, 0.97791, 0.86722, 0.01655, 0.43817, 0.69767, 0.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.06782, 0.82654, 0.12942, 0.17726, 0.11326, 0.17282, 0.00038, 0.81088, 0.9816, 0.40945, 0.74331, 0.80034, 0.71325, 0.91449, 0.12842, 0.29639, 0.93443, 0.70015, 0.47373, 0.48878, 0.75053, 0.52359, 0.29784, 0.39894, 0.56431, 0.85548, 0.79251, 0.1631, 0.38654, 0.50632, 0.26896, 0.34458, 0.21217, 0.6246234234, 0.24252, 0.06612, 0.49736, 0.32115, 0.05175, 0.74311, 0.46243, 0.46945, 0.8904, 0.52333, 0.3, 0.3, 0.3, 0.3, 0.90865, 0.67153, 0.01126, 0.97171, 0.87841, 0.49106, 0.13053, 0.17982, 0.82662, 0.28247, 0.86139, 0.56019, 0.50764, 0.77718, 0.85172, 0.41824, 0.25684, 0.5, 0.4, 0.3, 0.55297, 0.8503, 0.30904, 0.99926, 0.85589, 0.444, 0.01316, 0.09911, 0.555, 0.87012, 0.41096, 0.48637, 0.85519, 0.47088, 0.1011, 0.25033, 0.09467, 0.40198, 0.96851, 0.82213, 0.12503, 0.20571, 0.25076, 0.06231, 0.07601, 0.45708, 0.11272, 0.63568, 0.23461, 0.34695, 0.09066, 0.43258, 0.8, 0.8, 0.8, 0.81373, 0.80286, 0.96214, 0.88751, 0.1231, 0.18324, 0.65326, 0.15867, 0.38488, 0.65268, 0.32696, 0.94382, 0.53507, 0.76713, 0.14548, 0.48512, 0.9634, 0.06756, 0.072, 0.39152, 0.31019, 0.6, 0.7, 0.49246, 0.228802, 0.08583, 0.03398, 0.0285, 0.5462, 0.24258, 0.14214, 0.07815, 0.4124, 0.123, 0.93681, 0.57008, 0.31158, 0.54264, 0.15469, 0.55414, 0.91683, 0.51145, 0.41477, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.58764, 0.88313, 0.37205, 0.02449, 0.52112, 0.87728, 0.777, 0.55553, 0.66, 0.02313, 0.11111, 0.80667, 0.53751, 0.0131, 0.65933, 0.18781, 0.74947, 0.96709, 0.80491, 0.6905, 0.9895, 0.04426, 0.39591, 0.42531, 0.30839, 0.56514, 0.63484, 0.7866, 0.68256, 0.10216, 0.48288, 0.35511, 0.60479, 0.11373, 0.24926, 0.7167, 0.42896, 0.17249, 0.53224, 0.65764, 0.37756, 0.8888, 0.1, 0.1, 0.1, 0.3539, 0.88888, 0.24885, 0.76737, 0.16757, 0.78549, 0.41, 0.1, 0.1, 0.1, 0.32993, 0.67534, 0.71187, 0.43277, 0.8, 0.666, 0.13769, 0.92555453, 0.82044, 0.911, 0.87363, 0.39582, 0.10465, 0.8, 0.7, 0.58114, 0.6, 0.2, 0.2, 0.3, 0.2, 0.1, 0.3, 0.8, 0.7, 0.6, 0.5, 0.4]}' "http://127.0.0.1:5000/"
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
