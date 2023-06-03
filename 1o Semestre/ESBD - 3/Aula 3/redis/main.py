import json
import random

from faker import Faker
from redis import Redis

FAKE = Faker("pt_BR")


def rand_cpf():
    return random.randint(111, 999)


def main():
    redis_client = Redis(host="127.0.0.1", port=6379, db=0)

    cpfs = []
    for _ in range(100):
        cpf = f"{rand_cpf()}.{rand_cpf()}.{rand_cpf()}-{random.randint(11,99)}"
        while cpf in cpfs:
            cpf = f"{rand_cpf()}.{rand_cpf()}.{rand_cpf()}-{random.randint(11,99)}"

        cpfs.append(cpf)

        usr_dict = {"name": FAKE.name(), "address": FAKE.address()}
        redis_client.set(f"user:{cpf}", json.dumps(usr_dict))

    # for key in redis_client.scan_iter("user:*"):
    #     print(key.decode("utf-8"))
    #     print(json.loads(redis_client.get(key)))


if __name__ == "__main__":
    main()