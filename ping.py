import sys
from tabulate import tabulate
import ipaddress
import subprocess


ip_addr_list = ['192.168.0.1', '7.7.7.7', '6.6.6.6']


def host_ping(host_list: list):
    """
    Функция проверяющая доступность узлов и отображающая информацию их пинга.
    Передается список адресов, по которым создаются ip-адреса и проверяется их пинг.
    :param host_list:
    :return:
    """

    for host in host_list:
        try:
            ip = ipaddress.ip_address(host)
            param = '-c'
            command = ['ping', param, '1', str(ip)]
            # Функция call возвращает число, если узел доступен. Если число равно 1, то это True и узел недоступен
            if subprocess.run(command).returncode:
                print('Узел недоступен')
            else:
                print('Узел доступен')
        except ValueError:
            print('Неверно указан ip адрес')


# Для выполнения 2 и 3 задания, я создам базовую функцию reachable_host_list и две функции для отображения
# данных в нужном формате
def reachable_host_list(host: str, from_oct: int, to_oct: int):
    """
    Функция проверяющая ip-адреса на доступность.
    Возвращает кортеж с доступными и недоступными адресами по выбранному хосту.

    :param host:
    :param from_oct:
    :param to_oct:
    :return:
    """
    # Списки доступных и недоступных адресов
    reachable = []
    unreachable = []
    print('Идет обработка данных подождите...')

    for h in range(from_oct, to_oct + 1):
        full_host = f'{host}{h}'
        try:
            ip = ipaddress.ip_address(full_host)
            param = '-c'
            command = ['ping', param, '1', str(ip)]

            # stdout отвечает за вывод сообщений на экран, subprocess.DEVNULL является null значением, тем самым мы
            # запрещаем вывод информации о пинге и добавляем доступный хост в результирующий список
            if not subprocess.run(command, stdout=subprocess.DEVNULL).returncode:
                reachable.append(full_host)
            else:
                unreachable.append(full_host)
        except ValueError:
            print('Неверно указан ip адрес')

    return reachable, unreachable


def host_range_ping(reachable_list):
    """
    Выводит сообщение показывающее список доступных адресов
    :param reachable_list:
    :return:
    """

    print(f'Вот список проверенных ip-адресов по вашему хосту:')
    for addr in reachable_list:
        print(addr)


def host_range_ping_tab(host_lists_reach: tuple):
    """
    Выводит сообщение показывающее таблицу доступных и недоступных адресов.
    :param host_lists_reach:
    :return:
    """

    reach = tabulate(host_lists_reach[0], headers='Reachable', tablefmt='plain').replace(' ', '')
    unreach = tabulate(host_lists_reach[1], headers='Unreachable', tablefmt='plain').replace(' ', '')
    print(f'\n{reach}\n\n{unreach}')


if __name__ == '__main__':
    message = 'Список доступных функций:\nhp: host_ping\nhrp: host_range_ping\nhrpt: host_range_ping_tab'

    # Берем первый хост из списка вначале для примера
    address = ip_addr_list[0][:-1]

    try:
        if sys.argv[1] == 'hp' or sys.argv[1] == 'host_ping':
            host_ping(ip_addr_list)
        elif sys.argv[1] == 'hrp' or sys.argv[1] == 'host_range_ping':
            # Получаем кортеж списков с ip-адресами
            host_list_done = reachable_host_list(address, 1, 5)
            host_range_ping(host_list_done[0])
        elif sys.argv[1] == 'hrpt' or sys.argv[1] == 'host_range_ping_tab':
            # Получаем кортеж списков с ip-адресами
            host_list_done = reachable_host_list(address, 1, 5)
            host_range_ping_tab(host_list_done)
        else:
            print(f'Такой функции нет в наличии.\n{message}')

    except IndexError:
        print('Для запуска используйте команду в терминале: python3 ping.py {название функции, '
              'которую хотите использовать}', f'\n{message}')
