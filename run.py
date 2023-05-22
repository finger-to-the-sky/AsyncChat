"""Программа-лаунчер"""

import subprocess
import time

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'python3 server.py']))
        time.sleep(1)
        PROCESSES.append(subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'python3 client.py']))
        time.sleep(4)
        PROCESSES.append(subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'python3 client.py']))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()