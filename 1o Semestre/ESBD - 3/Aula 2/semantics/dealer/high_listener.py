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
HIGH_TOPIC = "high_transactions"


def main():
    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": f"python-consumer-{str(uuid4())}",
            "auto.offset.reset": "latest",  # NOTE A DIFERENÇA AQUI!!! "latest"
        }
    )
    print("Kafka Consumer has been initiated...")

    print("Available topics to consume: ", c.list_topics().topics)
    c.subscribe([TOPIC, HIGH_TOPIC])

    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue

        if msg.error():
            print("Error: {msg.error()}")
            continue

        msg_data = msg.value().decode("utf-8")
        msg_epoch = msg.timestamp()[-1]
        if msg.topic() == HIGH_TOPIC:
            print(f"\n##### - {HIGH_TOPIC} - #####\n\n")

            print(msg_epoch)
            pprint(msg_data)

    c.close()


if __name__ == "__main__":
    main()
