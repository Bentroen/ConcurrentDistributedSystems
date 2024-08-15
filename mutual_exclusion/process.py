import os
from datetime import datetime
from time import sleep

COORDINATOR_PORT = 1234
PROCESS_ID = os.getpid()
SLEEP_TIME = 5


def acquire_lock():
    pass


def main():
    while True:
        # acquire critical region

        lock = False

        with lock:
            current_time = datetime.now()
            current_time_ms = current_time.time()
            line = f"[{PROCESS_ID}] {current_time_ms}"
            # Emitir mensagem para escrever o resultado
            # send_message("WRITE", )

        sleep(SLEEP_TIME)
