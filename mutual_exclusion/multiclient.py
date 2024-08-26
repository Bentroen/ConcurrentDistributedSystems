import os
from multiprocessing import Process

from mutual_exclusion.client import client_program

PROCESS_ID = os.getpid()

NUM_WORKERS = 5


def main():
    # Create three worker processes
    workers = []
    for _ in range(NUM_WORKERS):
        worker = Process(target=client_program, args=())
        workers.append(worker)
        worker.start()

    # Wait for the coordinator and workers to finish
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
