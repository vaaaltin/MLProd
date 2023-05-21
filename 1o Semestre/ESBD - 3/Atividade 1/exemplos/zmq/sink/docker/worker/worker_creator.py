from multiprocessing import Process

from shell import run_cmd
from worker import work


def main():
    count = 0
    while True:
        input("Clique [ENTER] para criar um novo worker")

        run_cmd(
            f"docker run -d --network host --name=zmq_worker_{count} my_zmq_worker"
        )

        count += 1


if __name__ == "__main__":
    main()
