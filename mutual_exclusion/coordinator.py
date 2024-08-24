import os
import socket
import threading
from datetime import datetime
from time import sleep

from mutual_exclusion.socket import SocketHandler

HOST = "localhost"
PORT = 1234

MESSAGE_LENGTH = 10

requests = []


def write_line_to_result(line: str):
    """Região crítica do processo. Escreve uma linha para o arquivo resultado.txt"""

    # TODO: quem deve escrever no arquivo é o processo, não o coordenador!
    # O coordenador só deve coordenar a exclusão mútua entre os processos
    # e salvar um log de todas as mensagens recebidas e enviadas

    with open("resultado.txt", "a") as f:
        f.writelines([line])


def coordinator_thread():
    """Loop de execução da thread que coordena a exclusão mútua entre os processos"""

    # TODO: Essa thread deve ser criada dinamicamente para atender cada chamada!

    # Processo dorme por um tempo, e envia a mensagem REQUEST
    # Aguarda até que o coordenador envie a mensagem GRANT
    # Processo entra na região crítica, escreve e aguarda um tempo
    # Processo envia a mensagem RELEASE

    lock = threading.Lock()

    # Acompanhar lista de requisições
    while True:
        if len(requests) > 0:
            # Não precisa ter um lock aqui, pois o coordenador gerencia a exclusão mútua
            request = requests.pop(0)
            print("Processing request:", request)


def process_listener_thread():
    """Loop de execução da thread que recebe novos processos"""


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(" -> ")
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get the local machine name
    port = 12397  # Reserve a port for your service
    s.bind((host, port))  # Bind to the port

    s.listen(3)  # Wait for the client connection
    conn, address = server_socket.accept()  # Establish connection with client.
    print("Got connection from", address)

    while True:
        c, addr = s.accept()  # Establish a connection with the client
        print("Got connection from", addr)
        c.send("Thank you for connecting!")

        # Receber a mensagem do processo
        message = c.recv(MESSAGE_LENGTH).decode("utf-8")
        print("Received message:", message)

        # Adicionar a mensagem à lista de requisições
        requests.append(message)

    c.close()

    while False:
        pass

    # TODO: Criar uma nova thread para atender a requisição
    # Duas threads estáticas, uma dinâmica (criada sob demanda!)

    t1 = threading.Thread(target=coordinator_thread, name="t1")
    t1.start()
    t1.join()


def ui_thread():
    """Loop de execução da thread de interface"""

    return

    while True:
        current_time = datetime.now()
        current_time_ms = current_time.time()
        print("UI thread running at", current_time_ms)
        sleep(2)


class CoordinatorThread(threading.Thread):
    pass


def main():
    print("Coordinator process spawned with ID:", os.getpid())
    print("Main thread name:", threading.current_thread().name)

    # t1 = threading.Thread(target=coordinator_thread, name='t1')
    t2 = threading.Thread(target=process_listener_thread, name="t2")
    t3 = threading.Thread(target=ui_thread, name="t3")

    # t1.start()
    t2.start()
    t3.start()

    # t1.join()
    t2.join()
    t3.join()


if __name__ == "__main__":
    main()
