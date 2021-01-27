# This file is part of Neotest.
# See http://www.neotest.io for more information.
# This program is published under the MIT license.

from time import sleep

from pbr.version import VersionInfo

from . import logging  # isort:skip - circular import dependency
from . import bases  # isort:skip - circular import dependency
from . import executor  # isort:skip - circular import dependency

__all__ = ["logging", "bases", "executor", "sleep"]

# Check the PBR version module docs for other options than release_string()
__version__ = VersionInfo("neotest").release_string()

if __name__ == "__main__":
    from neotest.main import main

    main()
