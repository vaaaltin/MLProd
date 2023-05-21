# https://redis.io/docs/stack/get-started/install/docker/
# docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
# docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

import json
import random
from datetime import datetime
from time import sleep

import redis


def main():


    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        msg = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "data": {
                "type": random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                "value": random.randint(0, 999)
            }
        }

        redis_client.publish(
            "transactions",
            json.dumps(msg)
        )

        sleep(random.randint(1, 5))


if __name__ == '__main__':
    main()