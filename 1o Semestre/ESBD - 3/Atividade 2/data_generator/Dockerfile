FROM python:3.7

RUN pip install pandas confluent-kafka

COPY . .

CMD ["python", "-u", "main.py"]