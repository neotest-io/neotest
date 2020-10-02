# This file is part of Neotest
# See http://www.neotest.io for more information
# This program is published under the MIT license

import builtins
import logging

__all__ = ["Log"]

logging.PRINT: int = 1
logging.addLevelName(logging.PRINT, "PRINT")

logging.basicConfig(
    level=logging.PRINT,
    format=""
    "%(asctime)s "
    "%(relativeCreated)d "
    "%(name)s "
    "%(threadName)s "
    "%(filename)s:%(lineno)d:%(funcName)s() "
    "%(levelname)s: %(message)s",
)

log_default: str = "neotest"


def my_print(message: str, *args, **kwargs):
    logging.log(logging.PRINT, message, *args, **kwargs)


class Log(object):
    """
    Wrapper over standard logging module
    """

    def __init__(self, name: str = log_default, print_override: bool = True):
        if name == log_default:
            self._name = name
        else:
            self._name = log_default + "." + name

        self._logger = logging.getLogger(self._name)

        if print_override:
            self._print_override()

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)

    def print(self, message: str):
        self._logger.log(logging.PRINT, message)

    def _print_override(self):
        if not hasattr(builtins, "__print__"):
            builtins.__print__ = builtins.print

        builtins.print = my_print

    def _print_restore(self):
        builtins.print = builtins.__print__
