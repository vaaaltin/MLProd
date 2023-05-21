FROM python:3

RUN pip install pyzmq

COPY worker.py worker.py

CMD [ "python", "-u", "worker.py"]