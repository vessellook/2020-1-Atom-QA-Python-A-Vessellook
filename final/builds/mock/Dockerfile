FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "vk_api_mock.py"]

COPY vk_api_mock.py .
