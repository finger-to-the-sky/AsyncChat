import dis
import sys
from socket import socket, AF_INET, SOCK_STREAM
# import threading
import time
import logging
import json
from other.variables import ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, MESSAGE, MESSAGE_TEXT, \
    ERROR, DESTINATION, EXIT
from other.utils import get_message, send_message
from other.command_arguments import arguments
import log.client_log_config
from log.decorator import log


class ClientVerifier(type):
    def __init__(cls, name, bases, namespace):
        allow_methods = []
        for method in namespace:
            try:
                ret = dis.get_instructions(namespace[method])
                for i in ret:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in allow_methods:
                            allow_methods.append(i.argval)
            except TypeError:
                pass

        if 'accept' in allow_methods:
            raise TypeError('Method accept error')
        elif 'listen' in allow_methods:
            raise TypeError('Method listen error')

        if 'get_message' not in allow_methods and 'send_message' not in allow_methods:
            raise TypeError('Sockets error')

        super().__init__(name, bases, namespace)


class Client(metaclass=ClientVerifier):
    LOGGER = logging.getLogger('client')

    def __init__(self, server_address, server_port, client_name=None, mode='read'):
        self.server_address = server_address
        self.server_port = server_port
        self.client_name = client_name
        self.mode = mode

    @log
    def message_from_server(self, sock, my_username):
        """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
        while True:
            try:
                message = get_message(sock)
                if ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                          f'\n{message[MESSAGE_TEXT]}')
                    self.LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                                     f'\n{message[MESSAGE_TEXT]}')
                else:
                    self.LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                self.LOGGER.critical(f'Потеряно соединение с сервером.')
                break

    @log
    def create_message(self, sock, account_name):
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
        self.LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(sock, message_dict)
            self.LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            self.LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    @staticmethod
    def create_exit_message(username):
        """Функция создаёт словарь с сообщением о выходе"""
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: username
        }

    @log
    def user_interactive(self, sock, username):
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message(sock, username)
            elif command == 'exit':
                send_message(sock, self.create_exit_message(username))
                print('Завершение соединения.')
                self.LOGGER.info('Завершение работы по команде пользователя.')
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды.')

    @log
    def create_presence(self, account_name):
        """Функция генерирует запрос о присутствии клиента"""
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        self.LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out

    @log
    def process_response_ans(self, message):
        """
        Функция разбирает ответ сервера на сообщение о присутствии,
        возвращает 200 если все ОК или генерирует исключение при ошибке
        """
        self.LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            elif message[RESPONSE] == 400:
                raise Exception(f'400 : {message[ERROR]}')
        raise Exception(RESPONSE)

    def main(self):
        """
        Главная функция для чтения сообщений других пользователей
        """

        print('Консольный мессенджер. Клиентский модуль.')
        if self.mode == 'send':
            print('Отправка сообщений.')
        if not self.client_name:
            self.client_name = input('Введите имя пользователя: ')

        self.LOGGER.info(
            f'Запущен клиент с параметрами: адрес сервера: {self.server_address}, '
            f'порт: {self.server_port}, имя пользователя: {self.client_name}')

        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((self.server_address, self.server_port))
            send_message(client_socket, self.create_presence(self.client_name))
            answer = self.process_response_ans(get_message(client_socket))
            self.LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
            print(f'Установлено соединение с сервером.')
        except (ConnectionRefusedError, ConnectionError):
            self.LOGGER.critical(
                f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}, '
                f'конечный компьютер отверг запрос на подключение.')
            sys.exit(1)
        else:
            if self.mode == 'send':

                self.user_interactive(client_socket, self.client_name)
            else:
                self.message_from_server(client_socket, self.client_name)
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
    host, port, name, cli_mode = arguments()
    cli = Client(host, port, name, cli_mode)
    cli.main()
