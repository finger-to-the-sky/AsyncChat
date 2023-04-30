import datetime
import argparse
import json
from socket import *
from log.client_log_config import client_log


def client_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    args = parser.parse_args()
    return args


def connect_to_server(host, port):
    connected_server = socket(AF_INET, SOCK_STREAM)
    connected_server.connect((host, int(port)))
    return connected_server


def requests_client(client_server, response_message: dict):
    client_server.send(json.dumps(response_message).encode('UTF-8'))
    data = client_server.recv(10000)
    valid_data = json.loads(data)
    client_log(f'Response from server: status code: {valid_data["response"]}, length: {len(data)} bytes')

    client_server.close()


if __name__ == '__main__':
    arguments = client_arguments()
    server = connect_to_server(arguments.a, arguments.p)

    message = {
        "action": "presence",
        "time": str(datetime.date.today()),
        "type": "status",
        "user": {
            "account_name": "C0deMaver1ck",
            "status": "Yep, I am here!"
        }
    }
    requests_client(server, message)
