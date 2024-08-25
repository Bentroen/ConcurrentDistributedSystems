import os
import socket
import threading
from queue import Queue
from typing import Tuple

from mutual_exclusion.util import MESSAGE_LENGTH, MessageType, format_message


class CoordinatorThreadState:
    IDLE = 1  # No process in the critical section
    BUSY = 2  # There's a process in the critical section


def coordinator(requests_queue: list[str], release_queue: list[str]):
    # Process requests in the requests list

    print("[Coordinator] Coordinator thread started")

    status = CoordinatorThreadState.IDLE

    while True:
        if (
            status == CoordinatorThreadState.BUSY
        ):  # Wait for a release message from the process
            if release_queue.empty():
                continue

            # Get the first release from the list
            proc_id = release_queue.get()
            print("[Coordinator] Received release from process", proc_id)

            # Return to the idle state
            print("[Coordinator] Returning to idle state")
            status = CoordinatorThreadState.IDLE

        elif status == CoordinatorThreadState.IDLE:
            # Check if there are any requests in the list
            if requests_queue.empty():
                continue

            # Get the first request from the list
            proc_id, conn = requests_queue.get()  # block=True

            # Send a grant message to the requesting process
            print("[Coordinator] Received request from process", proc_id)
            grant_message = format_message(MessageType.GRANT, int(proc_id))
            print("[Coordinator] Sending grant to process", proc_id)
            status = CoordinatorThreadState.BUSY
            conn.send(grant_message)
            print("[Coordinator] Grant sent to process", proc_id)


def process_listener(
    conn: socket.socket, address: str, requests_queue: Queue, release_queue: Queue
):
    # Listens for incoming messages from the connected client (recv)
    # and adds it to the requests list
    while True:
        data = conn.recv(MESSAGE_LENGTH).decode()
        if not data:
            print("Connection closed with client:", address)
            break
        print(f"From {address}: {str(data)}")

        # Check if the message is a request and add it to the requests list
        message_type, proc_id, _ = data.split("|")
        print("Received message from process", proc_id)

        if message_type == str(MessageType.REQUEST.value):
            print("Adding request to the queue")
            requests_queue.put((proc_id, conn))

        elif message_type == str(MessageType.RELEASE.value):
            print("Received release message from process", proc_id)
            release_queue.put(proc_id)
    conn.close()


def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server process started!")

    connections = []
    requests_queue = Queue(maxsize=10)
    release_queue = Queue(maxsize=10)

    coordinator_thread = threading.Thread(
        target=coordinator, args=(requests_queue, release_queue)
    )
    coordinator_thread.start()

    # Accept connections from multiple clients
    while True:
        print("Waiting for connection...")
        conn, address = server_socket.accept()
        print("Got connection from:", address)
        connections.append(conn)

        # Create a new thread to handle the client
        client_thread = threading.Thread(
            target=process_listener, args=(conn, address, requests_queue, release_queue)
        )
        client_thread.start()


def clear_result():
    with open("resultado.txt", "w") as file:
        file.write("")


if __name__ == "__main__":
    clear_result()
    server_program()
