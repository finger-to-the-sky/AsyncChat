import argparse
import sys

from log.decorator import log


@log
def arguments():
    """
    Функция принятия и передачи аргументов сокетам с значениями по дефолту
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-m', '--mode', default='read', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_name = namespace.name
    mode = namespace.mode
    return server_address, int(server_port), client_name, mode

