import logging

def init_logger(name: str):
    logger = logging.getLogger(name)
    logging.Formatter(fmt="%(name)s(%(lineno)d)::%(levelname)-8s: %(message)s")
    return logger