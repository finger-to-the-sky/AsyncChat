import argparse
import socket
from socket import *
import json
from log.server_log_config import server_log


def server_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    args = parser.parse_args()
    return args


def server_init(host: str, port: int):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen(3)
    return server


def requests_server(server_socket, response_message: dict):
    while True:
        client, addr = server_socket.accept()
        data = client.recv(10000)
        valid_data = json.loads(data)
        server_log(f'Presence message from client: {valid_data}')
        client.send(json.dumps(response_message).encode('UTF-8'))

        client.close()


if __name__ == '__main__':
    arguments = server_arguments()
    main_server = server_init(arguments.a, int(arguments.p))
    message = {
        "response": 200,
        "alert": "Необязательное сообщение/уведомление"
    }
    requests_server(main_server, message)
