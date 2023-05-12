import logging
import sys
import log.client_log_config
import log.server_log_config


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        LOGGER.debug('Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}')
        return f
    return wrapper
