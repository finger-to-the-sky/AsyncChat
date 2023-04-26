import argparse
import socket
from socket import *
import json


def server(host, port):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, int(port)))
    server.listen(3)

    while True:
        client, addr = server.accept()
        data = client.recv(10000)
        valid_data = json.loads(data)
        print(f'Presence message from client: {valid_data}')
        msg = json.dumps({
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        })
        client.send(msg.encode('UTF-8'))

        client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    args = parser.parse_args()

    server(args.a, args.p)
