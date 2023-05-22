import sys
import socket
import threading
import time
import logging
import json
from other.variables import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, MESSAGE, MESSAGE_TEXT, ERROR, \
    DESTINATION, EXIT
from other.utils import get_message, send_message
from other.command_arguments import arguments
import log.client_log_config
from log.decorator import log


LOGGER = logging.getLogger('client')


@log
def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name):
    """
    Функция запрашивает кому отправить сообщение и само сообщение,
    и отправляет полученные данные на сервер
    :param sock:
    :param account_name:
    :return:
    """

    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


def create_exit_message(username):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }


@log
def user_interactive(sock, username):
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOGGER.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')


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
    возвращает 200 если все ОК или генерирует исключение при ошибке
    """
    LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise Exception(f'400 : {message[ERROR]}')
    raise Exception(RESPONSE)


def main():
    """
    Главная функция для чтения сообщений других пользователей
    """
    print('Консольный мессенджер. Клиентский модуль.')
    server_address, server_port, client_name = arguments()
    task = input('Выберите функцию:\n1.Чтение\n2.Запись\n')
    if not client_name:
        client_name = input('Введите имя пользователя: ')


    LOGGER.info(
        f'Запущен клиент с параметрами: адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {client_name}')

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_address, server_port))
        send_message(server_socket, create_presence(client_name))
        answer = process_response_ans(get_message(server_socket))
        LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except (ConnectionRefusedError, ConnectionError):
        LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if task == 'Запись':
            user_interactive(server_socket, client_name)
        else:
            message_from_server(server_socket, client_name)
        # receiver = threading.Thread(target=message_from_server, args=(server_socket, client_name))
        # receiver.daemon = True
        # receiver.start()
        #
        # user_interface = threading.Thread(target=user_interactive, args=(server_socket, client_name))
        # user_interface.daemon = True
        # user_interface.start()
        #
        # while True:
        #     time.sleep(1)
        #     if receiver.is_alive() and user_interface.is_alive():
        #         continue
        #     break


if __name__ == '__main__':
    main()
