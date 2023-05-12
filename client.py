import logging
import sys
import socket
import time
from other.variables import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, MESSAGE, MESSAGE_TEXT, ERROR
from other.utils import get_message
from other.command_arguments import arguments
import log.client_log_config
from log.decorator import log

LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""

    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
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
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence(account_name='Guest'):
    """Функция генерирует запрос о присутствии клиента"""
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_response_ans(message):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    """
    LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise Exception(message[ERROR])
    raise Exception('В принятом словаре отсутствует обязательное поле')


@log
def client_connection(server_address, server_port):
    """
    Функция установки подключения клиента к серверному сокету
    :param server_address:
    :param server_port:
    :return: client socket
    """

    LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}')
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
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            LOGGER.error('Соединение с сервером было потеряно.')
            sys.exit(1)


if __name__ == '__main__':
    client_arguments = arguments()
    main(client_connection(client_arguments[0], client_arguments[1]))
