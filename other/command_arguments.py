import argparse
from log.decorator import log


@log
def arguments():
    """
    Функция принятия и передачи аргументов сокетам с значениями по дефолту
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs='?', default='localhost')
    parser.add_argument('-p', default=8000)
    args = parser.parse_args()
    host, port = args.a, int(args.p)
    return [host, port]
