FROM python:3

RUN pip install pyzmq

COPY sink.py main.py

CMD [ "python", "-u", "main.py"]