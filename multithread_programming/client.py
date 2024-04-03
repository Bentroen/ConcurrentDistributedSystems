import random
import socket
import time
import logging


def client_process():
    host = "127.0.0.1"
    port = 12345

    logging.basicConfig(
        level=logging.DEBUG, format="[%(asctime)s] pid_%(process)d: %(message)s"
    )

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            message = "Can I get some service?"
            client_socket.send(message.encode())
            logging.info("Sent message: %s", message)

            response = client_socket.recv(1024).decode()
            logging.info("Server response: %s", response)

            sleep_time = random.randint(3, 8)
            logging.info("Sleeping for %d seconds\n", sleep_time)
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            break

    client_socket.close()


if __name__ == "__main__":
    client_process()
