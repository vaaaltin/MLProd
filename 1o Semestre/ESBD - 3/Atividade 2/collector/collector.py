import zmq
import json
import os
import random
import pandas as pd
import redis
from confluent_kafka import Producer


KAFKA_PUB_TOPIC = "fraud_credictcard_transactions"


def main():        
    context = zmq.Context()

    #pull the results
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://0.0.0.0:5346")

    kafka_producer = Producer(
        {
            "bootstrap.servers": "localhost:9092"
        }
    )
    while True:
        result = results_receiver.recv_json()

        if result["fraud"]:
            kafka_producer.produce(
                    KAFKA_PUB_TOPIC,
                    json.dumps(result).encode(),
                )
            print(f"Fraud detected and sended to database: {result}")
        else:
            print(result)

if __name__ == "__main__":
    main()