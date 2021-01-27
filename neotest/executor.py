# This file is part of Neotest.
# See http://www.neotest.io for more information.
# This program is published under the MIT license.

import neotest


class ExecutorProc(neotest.bases.ProcessBase):
    def __init__(self, name=None):
        neotest.bases.ProcessBase.__init__(self, name=name)

    def run(self):
        self.log.debug("%s(%d) says hello!" % (self.name, self.pid))


class ExecutorTh(neotest.bases.ThreadBase):
    def __init__(self, name=None):
        neotest.bases.ThreadBase.__init__(self, name=name)

    def run(self):
        self.log.debug("%s(%d) says hello!" % (self.name, self.native_id))
