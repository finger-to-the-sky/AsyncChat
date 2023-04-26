import datetime
import argparse
import json
from socket import *


def client(host, port):
    server = socket(AF_INET, SOCK_STREAM)
    server.connect((host, int(port)))
    msg = json.dumps({
        "action": "presence",
        "time": str(datetime.date.today()),
        "type": "status",
        "user": {
            "account_name": "C0deMaver1ck",
            "status": "Yep, I am here!"
        }
    })
    server.send(msg.encode('UTF-8'))

    data = server.recv(10000)
    valid_data = json.loads(data)
    print(f'Response from server: status code: {valid_data["response"]}, length: {len(data)} bytes')

    server.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    args = parser.parse_args()

    client(args.a, args.p)
