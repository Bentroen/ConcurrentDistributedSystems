import os
import socket
import threading

HOST = "localhost"
PORT = 5000

MESSAGE_LENGTH = 10


requests = []


class MySocket:
    def _init_(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host=HOST, port=PORT):
        self.sock.connect((host, port))

    # def send(self, msg):
    #    totalsent = 0
    #    while totalsent < MSGLEN:
    #        sent = self.sock.send(msg[totalsent:])
    #        if sent == 0:
    #            raise RuntimeError("socket connection broken")
    #        totalsent = totalsent + sent

    def receive(self):
        msg = self.sock.recv(MESSAGE_LENGTH)
        if msg == b"":
            raise RuntimeError("socket connection broken")
        return msg

        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b"":
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b"".join(chunks)


def write_line_to_result(line: str):
    """Região crítica do processo. Escreve uma linha para o arquivo resultado.txt"""

    with open("resultado.txt", "a") as f:
        f.writelines([line])


def coordinator_thread():
    """Loop de execução da thread que coordena a exclusão mútua entre os processos"""

    # GLAUCO: Essa thread deve ser criada dinamicamente para atender cada chamada!

    line = "aaa"  # ???
    write_line_to_result(line)


def process_listener_thread():
    """Loop de execução da thread que recebe novos processos"""

    # socket = MySocket().connect()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(HOST, PORT)

    while False:
        pass

    # TODO: Criar uma nova thread para atender a requisição
    # Duas threads estáticas, uma dinâmica (criada sob demanda!)

    t1 = threading.Thread(target=coordinator_thread, name="t1")
    t1.start()
    t1.join()


def ui_thread():
    """Loop de execução da thread de interface"""

    pass


class CoordinatorThread(threading.Thread):
    pass


def main():
    print("ID of process running main program:", os.getpid())
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


if __name__ == "_main_":
    main()
