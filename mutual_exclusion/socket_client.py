import os
import random
import socket
from datetime import datetime
from time import sleep

from mutual_exclusion.util import (
    MESSAGE_LENGTH,
    WRITE_COUNT,
    MessageType,
    format_message,
)

PROCESS_ID = os.getpid()


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    written_count = 0

    print("Process started with ID:", PROCESS_ID)

    while written_count < WRITE_COUNT:  # message.lower().strip() != "bye":

        sleep(3)

        # Create and send request message
        message = format_message(MessageType.REQUEST, PROCESS_ID)
        print("Sending request message...")
        client_socket.send(message)  # send message

        # Wait for grant message response
        grant_message = format_message(MessageType.GRANT, PROCESS_ID).decode()
        response = None
        while response != grant_message:
            response = client_socket.recv(MESSAGE_LENGTH).decode()  # receive response
            print("Received from server: " + response)  # show in terminal

        # Access granted
        print("Access granted!")
        print("Writing to file...")

        # Write current date and process ID to the file
        with open("resultado.txt", "a") as file:
            current_time = datetime.now()
            current_time_ms = current_time.time()
            line = f"[{PROCESS_ID}] {current_time_ms}"
            file.write(line + "\n")

            # Wait some time before releasing the file
            sleep(3)

        # Send release message
        print("Done writing. Sending release message...")
        release_message = format_message(MessageType.RELEASE, PROCESS_ID)
        client_socket.send(release_message)
        written_count += 1

        # Wait some time before restarting the process
        sleep_time = random.randint(1, 5)
        print(f"Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    client_program()
