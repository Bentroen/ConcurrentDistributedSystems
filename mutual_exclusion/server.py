import logging
import os
import socket
import sys
import threading
from queue import Queue

from mutual_exclusion.util import MESSAGE_LENGTH, MessageType, format_message

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("mutual_exclusion.log", "w")
fh.setLevel(logging.INFO)

# fh = logging.FileHandler("mutual_exclusion_full.log", "w")
# fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s -  %(asctime)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class CoordinatorThreadState:
    IDLE = 1  # No process in the critical section
    BUSY = 2  # There's a process in the critical section


def coordinator(
    requests_queue: list[str],
    release_queue: list[str],
    grants_per_process: dict[int, int],
):
    # Process requests in the requests list

    logger.debug("[Coordinator] Coordinator thread started")

    status = CoordinatorThreadState.IDLE

    while True:
        if (
            status == CoordinatorThreadState.BUSY
        ):  # Wait for a release message from the process
            if release_queue.empty():
                continue

            # Get the first release from the list
            proc_id = release_queue.get()
            logger.debug("[Coordinator] Received release from process %s", proc_id)

            # Return to the idle state
            logger.debug("[Coordinator] Returning to idle state")
            status = CoordinatorThreadState.IDLE

        elif status == CoordinatorThreadState.IDLE:
            # Check if there are any requests in the list
            if requests_queue.empty():
                continue

            # Get the first request from the list
            proc_id, conn = requests_queue.get()  # block=True

            # Send a grant message to the requesting process
            logger.debug("[Coordinator] Received request from process %s", proc_id)
            grant_message = format_message(MessageType.GRANT, int(proc_id))
            logger.debug("[Coordinator] Sending grant to process %s", proc_id)

            # Increase process grant count
            proc_id = int(proc_id)
            if proc_id not in grants_per_process:
                grants_per_process[proc_id] = 0
            grants_per_process[proc_id] += 1

            status = CoordinatorThreadState.BUSY
            conn.send(grant_message)
            logger.info("SEND - GRANT   %s|%s", MessageType.GRANT, proc_id)
            logger.debug("[Coordinator] Grant sent to process %s", proc_id)


def process_handler(
    conn: socket.socket, address: str, requests_queue: Queue, release_queue: Queue
):
    # Listens for incoming messages from the connected client (recv)
    # and adds it to the requests list
    while True:

        data = conn.recv(MESSAGE_LENGTH).decode()
        if not data:
            logger.debug("Connection closed with client: %s", address)
            break
        # logger.info("RECV %s", data)
        logger.debug(f"From {address}: {str(data)}")

        # Check if the message is a request and add it to the requests list
        message_type, proc_id, _ = data.split("|")
        logger.debug("Received message from process %s", proc_id)

        if message_type == str(MessageType.REQUEST.value):
            logger.debug("Adding request to the queue")
            logger.info("RECV - REQUEST %s|%s", message_type, proc_id)
            requests_queue.put((proc_id, conn))

        elif message_type == str(MessageType.RELEASE.value):
            logger.debug("Received release message from process %s", proc_id)
            logger.info("RECV - RELEASE %s|%s", message_type, proc_id)
            release_queue.put(proc_id)
    conn.close()


def process_listener(
    server_socket: socket.socket,
    connections: list[socket.socket],
    requests_queue: Queue,
    release_queue: Queue,
):
    while True:
        logger.debug("Waiting for connection...")
        conn, address = server_socket.accept()
        logger.debug("Got connection from: %s", address)
        connections.append(conn)

        # Create a new thread to handle the client
        client_thread = threading.Thread(
            target=process_handler, args=(conn, address, requests_queue, release_queue)
        )
        client_thread.start()


def ui(grants_per_process: dict[int, int], requests_queue: Queue):
    logger.debug("UI thread started")

    print("| 1. Print current request list")
    print("| 2. Print grants per process")
    print("| 3. Exit the program\n")

    while True:
        command = input("Enter a command: ")
        print("\n")
        if command == "1":
            print(
                "Current request list:\n",
                [int(request[0]) for request in requests_queue.queue],
            )
        elif command == "2":
            print("Grants per process:")
            for proc_id, grant_count in grants_per_process.items():
                print(f"  Process {proc_id}: {grant_count} grants")
        elif command == "3":
            print("Bye!")
            os._exit(0)
        else:
            print("Invalid command")
        print("\n")


def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    logger.debug("Server process started!")

    connections = []
    requests_queue = Queue(maxsize=10)
    release_queue = Queue(maxsize=10)
    grants_per_process: dict[int, int] = {}

    # Start coordinator thread
    coordinator_thread = threading.Thread(
        target=coordinator, args=(requests_queue, release_queue, grants_per_process)
    )
    coordinator_thread.start()

    # Start listener thread to accept incoming connections
    listener_thread = threading.Thread(
        target=process_listener,
        args=(server_socket, connections, requests_queue, release_queue),
    )
    listener_thread.start()

    # Start main UI logic
    ui(grants_per_process, requests_queue)


def clear_result():
    with open("resultado.txt", "w") as file:
        file.write("")


if __name__ == "__main__":
    clear_result()
    server_program()
