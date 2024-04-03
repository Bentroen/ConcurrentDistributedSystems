import socket
import threading
import logging


def format_addr(addr):
    return "{}:{}".format(*addr)


def handle_client(client_socket, client_addr):
    logging.info("Connection from %s", format_addr(client_addr))
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break
            logging.info(
                "Received request from %s: %s", format_addr(client_addr), request
            )
            response = f"Service provided by thread_{threading.get_ident()}"
            client_socket.send(response.encode())
        except KeyboardInterrupt:
            break

    client_socket.close()
    logging.info("Connection from %s closed", format_addr(client_addr))


def main():
    host = "127.0.0.1"
    port = 12345

    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info("Server listening on %s:%s", host, port)

    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, client_addr)
            )
            client_handler.start()
        except KeyboardInterrupt:
            break

    server_socket.close()
    logging.info("Server shut down")


if __name__ == "__main__":
    main()
