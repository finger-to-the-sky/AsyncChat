import sys

from other.command_arguments import arguments
from other.utils import send_message
from client import create_message, client_connection


def send(transport):
    """ Функция отправки сообщений """
    while True:
        try:
            send_message(transport, create_message(transport))
        except Exception:
            sys.exit(1)


if __name__ == '__main__':
    client_arguments = arguments()
    send(client_connection(client_arguments[0], client_arguments[1]))
