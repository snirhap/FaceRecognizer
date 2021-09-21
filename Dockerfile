FROM python:3.9.7-slim

WORKDIR /app

COPY . /app

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3"]

CMD [ "app.py" ]