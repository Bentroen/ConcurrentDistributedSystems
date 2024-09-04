import argparse
import os
from multiprocessing import Process

from mutual_exclusion.client import client_program
from mutual_exclusion.util import WRITE_COUNT

PROCESS_ID = os.getpid()

NUM_WORKERS = 5


# Add two args: --workers and --write-count


def main():
    parser = argparse.ArgumentParser(description="Run multiple client processes")
    parser.add_argument(
        "--workers", type=int, default=NUM_WORKERS, help="Number of worker processes"
    )
    parser.add_argument(
        "--writes", type=int, default=WRITE_COUNT, help="Number of writes to perform"
    )
    args = parser.parse_args()

    worker_count = args.workers
    write_count = args.writes

    print(f"Starting {worker_count} worker processes writing {write_count} times...")

    # Create three worker processes
    workers = []
    for _ in range(worker_count):
        worker = Process(target=client_program, args=(write_count,))
        workers.append(worker)
        worker.start()

    # Wait for the coordinator and workers to finish
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
