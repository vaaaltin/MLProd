from pprint import pprint
from uuid import uuid4

from confluent_kafka import Consumer

################
c = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": f"python-consumer-{uuid4()}",
        "auto.offset.reset": "latest",
    }
)
print("Kafka Consumer has been initiated...")

print("Available topics to consume: ", c.list_topics().topics)
c.subscribe(["user-tracker"])


def main():
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue

        if msg.error():
            print("Error: {msg.error()}")
            continue

        msg_data = msg.value().decode("utf-8")
        msg_epoch = msg.timestamp()[-1]

        print(msg_epoch)
        pprint(msg_data)

    c.close()


if __name__ == "__main__":
    main()
