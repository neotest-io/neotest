# This file is part of NeoTest.
# See http://www.neotest.io for more information.
# This program is published under the MIT license.

import argparse
import os
import sys

import neotest

__all__ = ["main"]

log = neotest.log


def _check_path_tests(test: str) -> str:
    if not (os.path.isdir(test) or os.path.isfile(test) or os.path.isfile(test + ".py")):
        raise argparse.ArgumentError("argument '%s' is not a file or directory path" % test)

    return test


def _check_path_file(file: str) -> str:
    print("checking file: %s" % file)

    if not os.path.isfile(file):
        raise argparse.ArgumentError("argument '%s' is not a file" % file)

    return file


def _check_path_dir(dir: str) -> str:
    print("checking dir: %s" % dir)

    if not os.path.isdir(dir):
        raise argparse.ArgumentError("argument '%s' is not a directory" % dir)

    return dir


def _abort(msg: str):

    print("error: %s" % msg)
    sys.exit(1)


def _args_parse_and_validate(cmdline: list = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NeoTest Automation Framework tool")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=neotest.__version__),
    )

    parser.add_argument(
        "-t",
        "--test",
        action="extend",
        dest="tests",
        default=[],
        required=True,
        nargs=argparse.ONE_OR_MORE,
        type=_check_path_tests,
        help="The id of the test that should be executed. The id of the test is "
        "derived from the test file name excluding the extension. May be "
        "specified multiple times. Parent directory names where test cases "
        "are located may also be specified.",
    )

    parser.add_argument(
        "-s",
        "--steps",
        action="extend",
        dest="steps",
        default=[],
        nargs=argparse.ONE_OR_MORE,
        type=int,
        help="A list of test steps to execute. This option is invalid for "
        "an execution started for more than one test.",
    )

    parser.add_argument(
        "-c",
        "--conf",
        action="store",
        dest="conf",
        default=None,
        type=_check_path_file,
        help="An arbitrary test configuration file that should be loaded. ",
    )

    parser.add_argument(
        "-p",
        "--path",
        action="extend",
        dest="paths",
        default=[],
        nargs=argparse.ONE_OR_MORE,
        type=_check_path_dir,
        help="Test and configuration files directory search path. May be " "specified multiple times.",
    )

    parser.add_argument(
        "-l",
        "--log",
        action="store",
        dest="log",
        default="print",
        choices=["print", "info", "debug", "cli"],
        help="Log filter for stdout runtime printed messages: "
        "  'print': will log only the \"print()\" statements (default option). "
        "  'info':  displays 'print' and INFO logs. "
        "  'cli':   displays commands used by CLI based interfaces. "
        "  'debug': displays 'print', 'info', 'cli' and DEBUG logs. "
        "Each logging level includes the previous except for 'cli'.",
    )

    parser.add_argument(
        "--log-path",
        action="store",
        dest="logpath",
        default=None,
        type=_check_path_dir,
        help="Directory in which test logs will be saved. Default is the ./logs directory.",
    )

    parser.add_argument(
        "--log-nosave",
        action="store_true",
        dest="lognosave",
        default=False,
        help="Use this flag to avoid log files being created. Usefull for long runs "
        "where lots of logs are generated and the performance is degraded by disk IO.",
    )

    parser.add_argument(
        "--label",
        action="store",
        dest="label",
        default=None,
        help="From a common resource pool only a subset of the resources identified " "by a label would be used.",
    )

    parser.add_argument(
        "-j",
        "--jenkins",
        action="store_true",
        dest="jenkins",
        default=False,
        help="This switch disables colored logging when using the tool from Jenkins jobs.",
    )

    args = parser.parse_args(cmdline)

    log.debug("--tests:      %s" % args.tests)
    log.debug("--steps:      %s" % args.steps)
    log.debug("--conf:       %s" % args.conf)
    log.debug("--paths:      %s" % args.paths)
    log.debug("--log:        %s" % args.log)
    log.debug("--log-path:   %s" % args.logpath)
    log.debug("--log-nosave: %s" % args.lognosave)
    log.debug("--label:      %s" % args.label)
    log.debug("--jenkins:    %s" % args.jenkins)

    return args


def main():
    args = _args_parse_and_validate()

    log.debug(args)


if __name__ == "__main__":
    main()
