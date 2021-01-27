# This file is part of Neotest
# See http://www.neotest.io for more information
# This program is published under the MIT license

from .wrapper import LogClientBase, LoggerThread, logging

__all__ = ["start", "stop", "getLogger", "getQueue", "LogClientBase"]

__logth_instance = None


def start(level=logging.PRINT):
    global __logth_instance

    if __logth_instance is None:
        __logth_instance = LoggerThread(level)
        __logth_instance.start()

    return __logth_instance


def getLogger(name=None):
    global __logth_instance

    if __logth_instance is None:
        raise AttributeError("logging is not started")

    return __logth_instance.getLogger(name=name)


def getQueue():
    global __logth_instance

    if __logth_instance is None:
        raise AttributeError("logging is not started")

    return __logth_instance.queue


def stop():
    global __logth_instance

    if __logth_instance is not None:
        __logth_instance.stop()
        __logth_instance = None
