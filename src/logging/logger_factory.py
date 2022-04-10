import logging


def get_logger(name, log_file=None):
    """
    Returns a logger with the given name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
