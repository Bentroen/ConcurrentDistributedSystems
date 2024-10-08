from enum import IntEnum

MESSAGE_LENGTH = 10

WRITE_COUNT = 3


class MessageType(IntEnum):
    REQUEST = 1
    GRANT = 2
    RELEASE = 3


def format_message(message_type: MessageType, process_id: int):
    message = f"{message_type}|{process_id}|".encode("utf-8")
    padded_message = message + b"0" * (10 - len(message))
    return padded_message
