import zmq
from minio import Minio
from model import main as run


def main():
    # minio_client = Minio(
    #     "localhost:8005",
    #     access_key="minio",
    #     secret_key="minio123",
    #     secure=False,
    # )
    # print("connected to minio")
    # # Download:
    # for item in minio_client.list_objects("flower-data", recursive=True):
    #     # print(f"Downloading: {item.object_name}")
    #     data = minio_client.fget_object(
    #         "flower-data",
    #         object_name=item.object_name,
    #         file_path=item.object_name.split(".", maxsplit=1)[-1],
    #     )

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect("tcp://0.0.0.0:5005")

    print("SOCKET CONNECTED")

    while True:
        socket.send(b"RDY")
        workload = socket.recv_json()
        print("RCVD workload")
        print(workload)
        run(model_name=workload["model_name"], epochs=workload["epochs"])
        # run(model_name=workload["model_name"], epochs=1)


if __name__ == "__main__":
    main()
