# This file is part of Neotest.
# See http://www.neotest.io for more information.
# This program is published under the MIT license.

import multiprocessing
import threading

import neotest


class ProcessBase(multiprocessing.Process, neotest.logging.LogClientBase):
    def __init__(self, name=None):
        multiprocessing.Process.__init__(self, name=name)
        # this creates self.log object
        neotest.logging.LogClientBase.__init__(self, logger="process", queue=neotest.logging.getQueue())


class ThreadBase(threading.Thread, neotest.logging.LogClientBase):
    def __init__(self, name=None):
        threading.Thread.__init__(self, name=name)
        # this creates self.log object
        neotest.logging.LogClientBase.__init__(self, logger="thread", queue=neotest.logging.getQueue())
