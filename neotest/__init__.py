# This file is part of Neotest
# See http://www.neotest.io for more information
# This program is published under the MIT license

from pbr.version import VersionInfo

from .logging import Log, log

__all__ = ["Log", "log"]

# Check the PBR version module docs for other options than release_string()
__version__ = VersionInfo("neotest").release_string()

if __name__ == "__main__":
    from neotest.main import main

    main()
