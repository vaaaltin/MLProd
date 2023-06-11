import itertools
import os
import pathlib
import pickle

import tqdm
import zmq
from minio import Minio

DATASET_URL = (
    "https://s3.amazonaws.com/content.udacity-data.com/courses/nd188/flower_data.zip"
)


def main():
    # epochs = [i for i in range(5, 30 + 1, 5)]
    epochs = [i for i in range(1, 4)]
    model_names = ["densenet", "vgg"]

    combos = list(itertools.product(epochs, model_names))

    workloads = []
    for combo in combos:
        workloads.append({"epochs": combo[0], "model_name": combo[1]})

    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind("tcp://*:5005")
    print("SOCKET BOUND")

    print(workloads)

    while workloads:
        print(len(workloads))
        _ = socket.recv()
        socket.send_json(workloads.pop())
        print("SNT workload")


if __name__ == "__main__":
    # client = Minio(
    #     "0.0.0.0:8005",
    #     access_key="minio",
    #     secret_key="minio123",
    #     secure=False,
    # )

    # flower_data = pathlib.Path("./flower_data")

    # items_list = [f for f in flower_data.rglob("*") if f.is_file()]
    # # print(items_list)

    # for item in tqdm.tqdm(items_list):
    #     # print(item)
    #     client.fput_object(
    #         "flower-data",
    #         object_name=f"flower-data/{item}",
    #         file_path=item,
    #     )

    main()
