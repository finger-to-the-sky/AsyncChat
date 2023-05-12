import logging
import sys
import os
sys.path.append('../')
from other import variables


client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(client_formatter)
stream_handler.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding='utf-8')
log_file.setFormatter(client_formatter)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(log_file)
LOGGER.setLevel(variables.LOGGING_LEVEL)


if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
