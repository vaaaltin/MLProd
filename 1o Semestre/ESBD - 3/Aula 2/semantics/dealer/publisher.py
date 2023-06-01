"""
PRODUCER
"""

# pip install confluent-kafka
import json
import random
import time

from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092"})
print("Kafka Producer has been initiated...")

TOPIC = "new_transactions"


def main():
    i = 0
    while True:
        input("type")
        row = [random.randint(1, 50_000), random.randint(50_000, 100_000)]
        data = {"vals": row}

        m = json.dumps(data)
        p.produce(TOPIC, m.encode("utf-8"))
        p.flush()
        print(f"Sent Transaction, id = {i}")
        i += 1
        time.sleep(0.1)


if __name__ == "__main__":
    main()
