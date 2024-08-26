import os
from multiprocessing import Process

from mutual_exclusion.client import client_program
from mutual_exclusion.server import server_program
from mutual_exclusion.util import PROCESS_COUNT

PROCESS_ID = os.getpid()


def main():
    # Create the coordinator process
    coordinator = Process(target=server_program, args=())
    coordinator.start()

    # Create three worker processes
    workers = []
    for _ in range(PROCESS_COUNT):
        worker = Process(target=client_program, args=())
        workers.append(worker)
        worker.start()

    # Wait for the coordinator and workers to finish
    coordinator.join()
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
