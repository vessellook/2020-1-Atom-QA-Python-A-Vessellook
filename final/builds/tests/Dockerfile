FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

RUN mkdir /my_tests

WORKDIR /my_tests

COPY code /my_tests

CMD [ "pytest", "-l", "-s", "-vv", "-rA",
               "--alluredir=/alluredir",
               "--clean-alluredir",
#              "-m", "mixed",
#              "-n", '3',
               "--video-enable"
    ]
