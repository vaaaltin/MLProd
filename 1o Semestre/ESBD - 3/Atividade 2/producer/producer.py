import json
import time
import zmq
import random
import redis
from time import sleep
from confluent_kafka import Consumer
from threading import Thread
from datetime import datetime
from uuid import uuid4

TOPIC = "creditcard_transactions"
MSGS_TO_SEND = []
SENT_MSGS = []
WORKER_TIMEOUT = 10

def get_seconds_from(epoch_num):
    delta = datetime.fromtimestamp(epoch_num) - datetime.now()
    return delta.total_seconds()


def dispatcher():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://0.0.0.0:5345")

    while True:
        if MSGS_TO_SEND:
            workload = MSGS_TO_SEND.pop()

            workload["timestamp"] = datetime.now().timestamp()

            zmq_socket.send_json(workload["msg"])
            SENT_MSGS.append(workload)


def requeuer():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        msgs_to_remove = []

        for workload in SENT_MSGS:
            if (
                get_seconds_from(workload["timestamp"]) > WORKER_TIMEOUT
            ):  # request timedout
                if not redis_client.get(
                    workload["msg"]["id"]
                ):  # not marked as completed
                    MSGS_TO_SEND.append(workload)
                    msgs_to_remove.append(workload)
                    print(f"[WARNING] Requeueing {workload['id']}.")

                else:  # timeout but completed
                    msgs_to_remove.append(
                        workload
                    )  # we remove this so we dont keep checking it

        for msg in msgs_to_remove:
            SENT_MSGS.remove(msg)



def producer():
    Thread(target=dispatcher).start()
    Thread(target=requeuer).start()

    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": f"creditcard-transactions-consumer-{uuid4()}",
            "auto.offset.reset": "latest",  # earliest
        }
    )
    print("Kafka Consumer has been initiated...")

    c.subscribe([TOPIC])

    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue

        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        msg_data = json.loads(msg.value().decode("utf-8"))
        # Apenas enfileiramos a mensagem para ser enviada depois
        MSGS_TO_SEND.append(
            {
                "msg": msg_data,
            }
        )

    c.close()



if __name__ == "__main__":
    producer()