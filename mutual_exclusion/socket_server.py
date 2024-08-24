import random
import socket
import threading
from time import sleep

MESSAGE_LENGTH = 10


def handle_client(conn: socket.socket, address: str):
    while True:
        data = conn.recv(10).decode()
        if not data:
            break
        print(f"From {address}: {str(data)}")
    conn.close()


def process_listener(connections: list[socket.socket]):
    # Listens for incoming messages from the connected clients (recv)

    while True:
        if not connections:
            continue
        for conn in connections:
            # Create one thread to listen each process
            data = conn.recv(10).decode()
        if not data:
            break
        print(f"Received from client: {data}")


def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server process started!")

    connections = []

    listener_thread = threading.Thread(target=process_listener, args=(connections,))
    listener_thread.start()
    # listener_thread.join()

    request_queue = []

    while True:
        print("Waiting for connection...")
        conn, address = server_socket.accept()
        print("Got connection from:", address)
        connections.append(conn)


if __name__ == "__main__":
    server_program()
