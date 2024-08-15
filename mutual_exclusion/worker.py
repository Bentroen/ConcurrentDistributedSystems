import os
import random
import socket
from datetime import datetime
from enum import IntEnum
from time import sleep

from mutual_exclusion.socket import SocketHandler

COORDINATOR_HOST = "localhost"
COORDINATOR_PORT = 1234
PROCESS_ID = os.getpid()
SLEEP_TIME = 5


def acquire_lock():
    pass


class MessageType(IntEnum):
    REQUEST = 0
    GRANT = 1
    RELEASE = 2


def encode_message(type: MessageType, process_id: int):
    return f"{type.value}|{process_id}".encode("utf-8")


def main():

    print(f"Worker process with ID {PROCESS_ID} started")

    # Handle socket connection
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        message = encode_message(MessageType.REQUEST, PROCESS_ID)

        client_socket.send(message.encode())  # send message

        data = client_socket.recv(1024).decode()
        print("Received from server: " + data)

        # if the message is a GRANT message, then we can proceed
        if data[0] == MessageType.GRANT:
            pass

    client_socket.close()  # close the connection

    # Connect to the coordinator
    # coordinator_socket = SocketHandler()
    # coordinator_socket.connect(COORDINATOR_HOST, COORDINATOR_PORT)

    while True:
        # acquire critical region

        # Enviar a mensagem REQUEST para o coordenador
        # Só pegar o lock e escrever quando receber a mensagem GRANT

        lock = False

        with lock:
            current_time = datetime.now()
            current_time_ms = current_time.time()
            line = f"[{PROCESS_ID}] {current_time_ms}"
            # Emitir mensagem para escrever o resultado
            # send_message("WRITE", )

        sleep(SLEEP_TIME)

        print(f"Process {PROCESS_ID} is back to work")
        wait_time = random.randint(1, 5)
        sleep(wait_time)


if __name__ == "__main__":
    main()
