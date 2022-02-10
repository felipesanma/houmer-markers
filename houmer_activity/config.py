import logging

from dotenv import dotenv_values


def get_env():
    return dotenv_values(".env")


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
