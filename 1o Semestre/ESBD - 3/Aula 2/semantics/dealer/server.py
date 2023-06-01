"""
DISPATCHER
"""

import json
from datetime import datetime
from pprint import pprint
from threading import Thread
from time import sleep
from uuid import uuid4

import redis
import zmq
from confluent_kafka import Consumer

TOPIC = "new_transactions"

WORKER_TIMEOUT_SECS = 15

MSGS = []
SENT_MSGS = []
DONE_EPOCHS = []

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.DEALER)
SOCKET.bind("tcp://*:5555")
print("SOCKET BOUND")


def dispatcher_thread():
    while True:
        if MSGS:
            msg = MSGS.pop()
            SOCKET.send(b"", zmq.SNDMORE)  # Necessário no modelo DEALER/REP
            SOCKET.send_json(msg)
            print("msg sent to worker client")
            SENT_MSGS.append(msg)

        sleep(0.1)


def reciever_thread():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        msg = SOCKET.recv_string()
        print(msg)
        DONE_EPOCHS.append(msg)
        # Store the message ID in Redis with an expiration time of 24 hours
        # redis_client.setex(msg, 24 * 60 * 60, 1)
        sleep(0.1)


def comparer_thread():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    while True:
        msgs_to_remove = []
        for msg in SENT_MSGS:
            timestamp = str(msg["epoch"])
            delta = datetime.fromtimestamp(int(timestamp)) - datetime.now()
            if (
                delta.total_seconds() >= WORKER_TIMEOUT_SECS
                and timestamp not in DONE_EPOCHS
            ):
                MSGS.append(msg)
                msgs_to_remove.append(msg)
                print(f"MSG {msg['epoch']} did not respond")

        for msg in msgs_to_remove:
            SENT_MSGS.remove(msg)

        sleep(0.5)


def main():
    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": f"python-consumer-{str(uuid4())}",
            "auto.offset.reset": "latest",  # NOTE A DIFERENÇA AQUI!!!
        }
    )
    print("Kafka Consumer has been initiated...")

    Thread(target=reciever_thread).start()
    Thread(target=dispatcher_thread).start()
    Thread(target=comparer_thread).start()

    print("Available topics to consume: ", c.list_topics().topics)
    c.subscribe([TOPIC])

    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue

        if msg.error():
            print("Error: {msg.error()}")
            continue

        msg_data = json.loads(msg.value().decode("utf-8"))
        msg_epoch = msg.timestamp()[-1]

        msg = {"data": msg_data, "epoch": msg_epoch}
        print(msg_epoch)
        pprint(msg_data)
        MSGS.append(msg)

    c.close()


if __name__ == "__main__":
    main()
