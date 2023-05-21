
# pip install confluent-kafka
import json
import random
import time

from confluent_kafka import Producer
from faker import Faker

fake = Faker()


p = Producer({"bootstrap.servers": "localhost:9092"})
print("Kafka Producer has been initiated...")


def main():
    for _ in range(10):
        data = {
            "user_id": fake.random_int(min=20000, max=100000),
            "user_name": fake.name(),
            "user_address": fake.street_address()
            + " | "
            + fake.city()
            + " | "
            + fake.country_code(),
            "platform": random.choice(["Mobile", "Laptop", "Tablet"]),
            "signup_at": str(fake.date_time_this_month()),
        }
        m = json.dumps(data)
        p.produce("user-tracker", m.encode())
        p.flush()
        time.sleep(3)


if __name__ == "__main__":
    main()