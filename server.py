from other.command_arguments import arguments
import socket
import select
import time

from other.utils import send_message, get_message
from other.variables import MAX_CONNECTIONS, ACTION, TIME, USER, \
    ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, MESSAGE, MESSAGE_TEXT, ERROR


def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and \
            message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return

    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return

    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        pass


def server_socket(addr: str, port: int):
    """
    Функция установки соединения сокета
    :param addr: Хост
    :param port: Порт
    :return: server socket
    """
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((addr, port))
    transport.settimeout(0.5)
    transport.listen(MAX_CONNECTIONS)
    return transport


def main(sock):
    """
    Главная функция работы сервера
    Списки для хранения клиентов и сообщений.
    Основной цикл программы сервера.
    Принимаем сообщения и если там есть сообщения кладём в словарь,
    если ошибка, исключаем клиента.
    Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
    :param sock: server socket
    """
    clients = []
    messages = []
    while True:
        try:
            client, client_address = sock.accept()
        except OSError:
            pass
        else:
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
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)

                except:
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    clients.remove(waiting_client)


if __name__ == '__main__':
    server_arguments = arguments()
    main(server_socket(server_arguments[0], server_arguments[1]))
