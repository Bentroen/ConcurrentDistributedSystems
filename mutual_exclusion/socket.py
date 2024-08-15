import socket
from typing import Optional


class SocketHandler:
    def __init__(
        self, sock: Optional[socket.socket] = None, message_length: int = 1024
    ):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.message_length = message_length

    def connect(self, host: str, port: int):
        self.sock.connect((host, port))

    def send(self, msg: bytes):
        if len(msg) == 0:
            raise ValueError("Cannot send empty message")
        if len(msg) != self.message_length:
            raise ValueError(f"Message should have length {self.message_length}")

        # Send in one go
        sent = self.sock.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def receive(self):
        msg = self.sock.recv(self.message_length)
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
