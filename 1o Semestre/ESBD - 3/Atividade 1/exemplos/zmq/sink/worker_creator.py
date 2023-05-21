from multiprocessing import Process

from worker import work


def main():
    count = 0
    while True:
        input("Clique [ENTER] para criar um novo worker")

        Process(target=work).start()
        count += 1
        print("worker count:", count)


if __name__ == "__main__":
    main()
