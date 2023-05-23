import dis
import logging
from other.command_arguments import arguments
import socket
import select
from other.utils import send_message, get_message
from other.variables import MAX_CONNECTIONS, ACTION, TIME, \
    USER, ACCOUNT_NAME, SENDER, PRESENCE, ERROR, MESSAGE, \
    MESSAGE_TEXT, RESPONSE_400, DESTINATION, RESPONSE_200, EXIT
import log.server_log_config
from log.decorator import log

LOGGER = logging.getLogger('server')


class ServerVerifier(type):
    def __init__(cls, name, bases, namespace):

        allow_methods = []
        attrs = []
        for method in namespace:
            try:
                ret = dis.get_instructions(namespace[method])
                for i in ret:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in allow_methods:
                            allow_methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
            except TypeError:
                pass
        if 'connect' in allow_methods:
            raise TypeError
        if 'sock' not in attrs:
            raise TypeError('Socket Error')
        super().__init__(name, bases, namespace)


class Port:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, obj, value):
        if not 1023 < value< 65536:
            LOGGER.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        obj.__dict__[self.name] = value


class Server(metaclass=ServerVerifier):
    port = Port()

    def __init__(self, addr: str, port: int):
        self.addr = addr
        self.port = port
        self.sock = None

    def server_socket(self):
        """
        Функция установки соединения сокета
        :return: server socket
        """
        LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.port}, '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        self.sock = transport
        self.sock.settimeout(0.5)
        self.sock.listen(MAX_CONNECTIONS)
        return self.sock

    @log
    def process_client_message(self, message, messages_list, client, clients, names):
        """
        Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
        проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
        :param message:
        :param messages_list:
        :param client:
        :param clients:
        :param names:
        :return:
        """
        LOGGER.debug(f'Разбор сообщения от клиента : {message}')

        if ACTION in message and message[ACTION] == PRESENCE and \
                TIME in message and USER in message:

            if message[USER][ACCOUNT_NAME] not in names.keys():
                names[message[USER][ACCOUNT_NAME]] = client

                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(client, response)
                clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and \
                DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            messages_list.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            clients.remove(names[message[ACCOUNT_NAME]])
            names[message[ACCOUNT_NAME]].close()
            del names[message[ACCOUNT_NAME]]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(client, response)
            return

    @log
    def process_message(self, message, names, listen_socks):
        """
        Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
        список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
        :param message:
        :param names:
        :param listen_socks:
        :return:
        """
        if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
            send_message(names[message[DESTINATION]], message)
            LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                        f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')

    def main(self, sock):
        """
        Главная функция работы сервера
        Списки для хранения клиентов и сообщений.
        Основной цикл программы сервера.
        Принимаем сообщения и если там есть сообщения кладём в словарь,
        если ошибка, исключаем клиента.
        Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        :param sock:
        """
        clients = []
        messages = []
        names = dict()

        while True:
            try:
                client, client_address = sock.accept()
            except OSError:
                pass
            else:
                LOGGER.info(f'Установлено соединение с ПК {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message),
                                                    messages, client_with_message, clients, names)
                    except Exception:
                        LOGGER.info(f'Клиент отключился от сервера.')
                        clients.remove(client_with_message)

            for i in messages:
                try:
                    self.process_message(i, names, send_data_lst)
                except Exception:
                    LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    clients.remove(names[i[DESTINATION]])
                    del names[i[DESTINATION]]
            messages.clear()


if __name__ == '__main__':
    server_arguments = arguments()
    s = Server(server_arguments[0], server_arguments[1])
    s.main(s.server_socket())
