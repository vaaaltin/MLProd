"""
WORKER
"""

import json

import redis
import zmq
from confluent_kafka import Producer

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://0.0.0.0:5555")
print("SOCKET CONNECTED")
redis_client = redis.Redis(host="localhost", port=6379, db=0)

PUB_TOPIC = "high_transactions"

p = Producer({"bootstrap.servers": "localhost:9092"})
print("Kafka Producer has been initiated...")

while True:
    # Wait for a request from the server
    request = socket.recv_json()
    print("Received request:", request)

    response = str(request["epoch"])

    # data = json.loads(request["data"])
    # input(f"Press [ENTER] to check redis for {response}")
    if redis_client.get(request["epoch"]):
        print("already rcvd")
    else:
        print("processing...")

        if request["data"]["vals"][0] > 30_000:
            request["result"] = "valor alto demais!"
            pub_msg = json.dumps(request)
            p.produce(PUB_TOPIC, pub_msg.encode("utf-8"))
            p.flush()
            print(f"published to {PUB_TOPIC}")

        # input("Press [ENTER] to send response back to the server and save to redis")
        # Store the message ID in Redis with an expiration time of 24 hours
        redis_client.setex(response, 24 * 60 * 60, 1)

    # Send the response back to the server
    socket.send_string(response)
