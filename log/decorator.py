import logging
from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.basicConfig(level='INFO')
        logger = logging.getLogger('log')

        filename = 'client_server.log'
        handler = logging.FileHandler(filename)

        format_ = logging.Formatter('%(asctime)s %(message)s')
        handler.setFormatter(format_)

        logger.addHandler(handler)
        logger.info(f'Функция {func.__name__} вызвана из функции main')

        f = func(*args, **kwargs)
        return f
    return wrapper
