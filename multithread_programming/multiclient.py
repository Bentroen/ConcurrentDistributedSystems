import multiprocessing

from client import client_process

NUM_CLIENTS = 4


def main():
    processes = []

    for _ in range(NUM_CLIENTS):
        process = multiprocessing.Process(target=client_process)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
