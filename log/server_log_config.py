import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level='INFO')
log = logging.getLogger('server')


def server_log(data):
    filename = 'server.log'
    handler = logging.FileHandler(filename)

    format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
    handler.setFormatter(format_)

    handler_2 = TimedRotatingFileHandler(filename, when="midnight", interval=1, backupCount=7)
    handler_2.suffix = "%Y-%m-%d"
    log.addHandler(handler)
    log.info(data)
    log.addHandler(handler_2)
