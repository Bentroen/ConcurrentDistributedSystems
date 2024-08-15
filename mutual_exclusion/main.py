# Spawn the coordinator process and three worker processes

import os
from datetime import datetime
from multiprocessing import Process, Queue
from threading import Thread
from time import sleep

from mutual_exclusion.coordinator import main as coordinator_loop
from mutual_exclusion.worker import main as worker_loop

PROCESS_ID = os.getpid()

NUM_WORKERS = 3


def main():
    # Create a queue to communicate with the coordinator
    q = Queue()

    # Create the coordinator process
    coordinator = Process(target=coordinator_loop, args=())
    coordinator.start()

    # Create three worker processes
    workers = []
    for _ in range(NUM_WORKERS):
        worker = Process(target=worker_loop, args=())
        workers.append(worker)
        worker.start()

    # Wait for the coordinator and workers to finish
    coordinator.join()
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
