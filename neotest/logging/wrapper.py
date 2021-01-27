# This file is part of Neotest.
# See http://www.neotest.io for more information.
# This program is published under the MIT license.

import builtins
import logging
import logging.handlers
import multiprocessing
import threading

__all__ = ["LoggerThread", "LogClientBase"]

# add a custom PRINT level just after INFO
logging.PRINT: int = logging.INFO + 1
logging.addLevelName(logging.PRINT, "PRINT")

# this is the base name for all loggers used in this application
log_root_name: str = "neotest"

# this is used to customize the logger object
loggerClass = logging.getLoggerClass()


# this function is used to override the normal builtin 'print'
def my_print(message: str, *args, **kwargs):
    kwargs["stacklevel"] = 3
    logging.log(logging.PRINT, message, *args, **kwargs)


# custom Logger class
class LoggerWrap(loggerClass):
    """
    Wrapper over standard logging module
    """

    def __init__(self, name, level=logging.NOTSET):

        loggerClass.__init__(self, name, level=level)

        self._print_overriden = False

    def print(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'PRINT'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.print("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.isEnabledFor(logging.PRINT):
            self._log(logging.PRINT, msg, args, **kwargs)

    def print_override(self):
        if not self._print_overriden:
            if not hasattr(builtins, "__print__"):
                builtins.__print__ = builtins.print

            builtins.print = my_print
            self._print_overriden = True

    def print_restore(self):
        if self._print_overriden:
            builtins.print = builtins.__print__


class ConsoleLogHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

        fmt = (
            "%(asctime)s "
            "%(relativeCreated)d "
            "%(name)-10s "
            "%(processName)s.%(threadName)s "
            "%(filename)s:%(lineno)d:%(funcName)s() "
            "%(levelname)s: "
            "%(message)s"
        )

        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)


class QueueLogHandler(logging.handlers.QueueHandler):
    def enqueue(self, record):
        """
        Enqueue a record and wait.
        """
        self.queue.put(record)


# log server thread
class LoggerThread(threading.Thread):
    def __init__(self, logLevel=logging.PRINT, name="LoggerThread"):
        threading.Thread.__init__(self, name=name)

        self.logLevel = logLevel

        # must be called only one time
        logging.setLoggerClass(LoggerWrap)

        self._main_logger = logging.getLogger()
        self._main_logger.setLevel(self.logLevel)

        ch = ConsoleLogHandler()
        ch.setLevel(self._main_logger.level)
        self._main_logger.addHandler(ch)

        # queue needed for all log clients
        self.queue = multiprocessing.Queue()

        # local logger
        self._local_logger = logging.getLogger("local")
        self._local_logger.level = logging.DEBUG
        self._local_logger.propagate = False
        self._local_logger.print_override()
        self._local_logger.addHandler(QueueLogHandler(self.queue))

    def getLogger(self, name=None):
        if not self._local_logger or not self.is_alive():
            raise AttributeError("logging is not started")

        if name is None:
            return self._local_logger
        else:
            return logging.getLogger("local.%s" % name)

    def run(self):
        while True:

            # wait for new log records
            log_record = self.queue.get()

            # None represents the close message
            if log_record is None:
                break

            # log record name manipulation
            lrn = log_record.name.split(".")
            if lrn[0] == "local":
                lrn[0] = log_root_name
            else:
                lrn.insert(0, log_root_name)
            log_record.name = ".".join(lrn)

            # handle log record with the main logger
            self._main_logger.handle(log_record)

    def stop(self):
        if self.is_alive():
            self.queue.put(None)
            self._local_logger.print_restore()


class LogClientBase:
    def __init__(self, queue, logger=None):

        # log object for this process or thread
        if logger is None:
            self.log = logging.getLogger(self.name)
        else:
            self.log = logging.getLogger("%s.%s" % (logger, self.name))

        self.log.level = logging.DEBUG
        self.log.propagate = False
        self.log.addHandler(QueueLogHandler(queue))
