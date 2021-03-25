FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

RUN mkdir /my_tests

WORKDIR /my_tests

COPY run_in_docker.sh /my_tests

CMD /my_tests/run_in_docker.sh

COPY code /my_tests
