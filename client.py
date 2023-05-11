import sys
import socket
import time
from other.variables import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, MESSAGE, MESSAGE_TEXT, ERROR
from other.utils import get_message
from other.command_arguments import arguments


def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""

    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')


def create_message(sock, account_name='Guest'):
    """ Функция запрашивает текст сообщения и возвращает его.
        Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    return message_dict


def create_presence(account_name='Guest'):
    """Функция генерирует запрос о присутствии клиента"""
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_response_ans(message):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    """

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise Exception(message[ERROR])
    raise Exception('В принятом словаре отсутствует обязательное поле')


def client_connection(server_address, server_port):
    """
    Функция установки подключения клиента к серверному сокету
    :param server_address:
    :param server_port:
    :return: client socket
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))
        print('Установлено соединение с сервером.')
    except Exception:
        pass
    else:
        return sock


def main(client_socket):
    """
    Главная функция для чтения сообщений других пользователей

    :param client_socket:
    :return:
    """
    print('Режим работы - приём сообщений.')
    while True:
        try:
            message_from_server(get_message(client_socket))
        except Exception:
            sys.exit(1)


if __name__ == '__main__':
    client_arguments = arguments()
    main(client_connection(client_arguments[0], client_arguments[1]))
