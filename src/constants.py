import logging
from sys import stdout

FORMAT: str = "[%(levelname)s - %(funcName)4s() ] %(message)s"
LOG_FILE: str = "/var/log/nam/logs.log"

HANDLERS: list = [
    logging.FileHandler(LOG_FILE),
    logging.StreamHandler(stdout)
]

LOG_LEVEL: int = logging.DEBUG