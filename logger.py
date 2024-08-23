import logging
from logging import handlers
import os
from datetime import datetime


def print_banner(log, lines=None, char='#', length=120):
    """ Function to print multi/single line text in a banner style """
    log.info(char * length)

    if not isinstance(lines, list):
        lines = [lines]

    for line in lines:
        log.info(char + line.center(length - 2, " ") + char)

    log.info(char * length)


def setup_logger(name, level='DEBUG', max_size=10485760, backup_count=5):
    """
    Function to set the logger config with the given name, level, max size, and backup count.
    This will return the logger object

    :param name: Name of the logger
    :param level: Logging level, e.g., INFO, DEBUG, ERROR
    :param max_size: Maximum size of the log file in bytes
    :param backup_count: Number of backup files to keep
    :return: Configured logger
    """

    # Create the logs dir if dont exist already
    log_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    # Frame today's date to append to the log filename
    datetime_str = datetime.now().strftime('%Y%m%d')
    log_file = f'{log_dir_path}/{name}_{datetime_str}.log'
    formatter = logging.Formatter('%(asctime)s %(filename)s %(lineno)4d %(levelname)s %(message)s')

    # Create a file handler that logs messages to a file, with rotation
    handler = handlers.RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
    handler.setFormatter(formatter)

    # Create a logger and set the logging level
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(level))
    logger.addHandler(handler)

    # Adding the stream handler to also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
