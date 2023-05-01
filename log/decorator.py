import logging
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.basicConfig(level='INFO')
        log = logging.getLogger('log')
        filename = 'client_server.log'
        handler = logging.FileHandler(filename)
        format_ = logging.Formatter('%(asctime)s %(message)s')
        handler.setFormatter(format_)
        log.addHandler(handler)
        log.info(f'Функция {func.__name__} вызвана из функции main"ых на серверной и клиентской '
                 f'сторонах при работе мессенджера.')
        f = func(*args, **kwargs)

        return f
    return wrapper
