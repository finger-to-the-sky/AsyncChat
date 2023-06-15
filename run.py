"""Программа-лаунчер"""

import subprocess
import time

PROCESSES = []


count = int(input('Введите количество клиентов: '))
while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'python3 server.py']))
        time.sleep(1)
        cli_command = ['gnome-terminal', '--', 'bash', '-c', 'python3 client.py']
        send_cli_command = ['gnome-terminal', '--tab', '--', 'bash', '-c', 'python3 client.py -m send']
        for i in range(count):
            PROCESSES.append(subprocess.Popen(cli_command))
            PROCESSES.append(subprocess.Popen(send_cli_command))

        time.sleep(1)
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
