from .config import data
from .logging import get_logger


def logger_for(name):
    return get_logger(name)
