import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
sys.path.append('../')
from other import variables

server_formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s")

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_formatter)
stream_handler.setLevel(logging.ERROR)
log_file = TimedRotatingFileHandler(path, encoding='utf-8', interval=1, when='D')

LOGGER = logging.getLogger('server')
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(log_file)
LOGGER.setLevel(variables.LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
