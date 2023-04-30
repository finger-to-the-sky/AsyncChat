import logging


def client_log(data):
    logging.basicConfig(level='INFO')
    log = logging.getLogger('client')

    filename = 'client.log'
    handler = logging.FileHandler(filename)

    format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
    handler.setFormatter(format_)
    log.addHandler(handler)
    log.info(data)
