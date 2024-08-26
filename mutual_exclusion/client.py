import logging
import os
import random
import socket
import sys
from datetime import datetime
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Print log to stdout
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(process)d] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


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

    logger.debug("Process started with ID: %s", PROCESS_ID)

    sleep(3)

    while written_count < WRITE_COUNT:  # message.lower().strip() != "bye":

        # Create and send request message
        message = format_message(MessageType.REQUEST, PROCESS_ID)
        logger.debug("Sending request message...")
        client_socket.send(message)  # send message

        # Wait for grant message response
        grant_message = format_message(MessageType.GRANT, PROCESS_ID).decode()
        response = None
        while response != grant_message:
            response = client_socket.recv(MESSAGE_LENGTH).decode()  # receive response
            logger.debug("Received from server: %s", response)  # show in terminal

        # Access granted
        logger.debug("Access granted!")
        logger.debug("Writing to file...")

        # Write current date and process ID to the file
        with open("resultado.txt", "a") as file:
            current_time = datetime.now()
            current_time_ms = current_time.time()
            line = f"[{PROCESS_ID}] {current_time_ms}"
            file.write(line + "\n")

            # Wait some time before releasing the file
            sleep(3)

        # Send release message
        logger.debug("Done writing. Sending release message...")
        release_message = format_message(MessageType.RELEASE, PROCESS_ID)
        client_socket.send(release_message)
        written_count += 1

        # Wait some time before restarting the process
        sleep_time = random.randint(1, 5)
        logger.debug(f"Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    client_program()
