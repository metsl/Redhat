#! /usr/bin/env python

import argparse
import logging
import sys
import re
import strategy

_logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_options():  # generating user-friendly commandline interface with additional output options
    parser = argparse.ArgumentParser(description="Utility that searches for lines matching regular expression")
    parser.add_argument("-r", "--regexp", help="regular expression", required=True)
    parser.add_argument("-f", "--files", nargs="*", help="text files", type=argparse.FileType('r'), default=sys.stdin)
    action = parser.add_mutually_exclusive_group(required=False)
    action.add_argument("-u", "--underscore", action="store_true", help="prints underscore under the matching text")
    action.add_argument("-c", "--color", action="store_true", help="highlights the matching text")
    action.add_argument("-m", "--machine", action="store_true", help="generates machine output format")
    options = parser.parse_args()
    return options


def print_matched_lines(opts, file_name, line_num, line):
    '''
    :param opts: arguments
    :param file_name: name of the file
    :param line_num: line number
    :param line: line
    :return: prints formatted line
    Strategy Design Pattern
    '''
    if re.match(opts.regexp, line):
        if opts.color:
            s = strategy.Color(file_name, line_num, line, opts.regexp)
        elif opts.underscore:
            s = strategy.Underscore(file_name, line_num, line, opts.regexp)
        elif opts.machine:
            s = strategy.Machine(file_name, line_num, line, opts.regexp)
        else:
            s = strategy.Simple(file_name, line_num, line, opts.regexp)
        s.print_line()


def main():
    opts = get_options()
    # _logger.debug("OPTIONS ARE: {}".format(opts))
    for f in opts.files:
        line_num = 0
        if not isinstance(f, str):
            lines = f.readlines()
            for line in lines:
                line_num += 1
                print_matched_lines(opts, f.name, line_num, line)
        else:
            line_num += 1
            print_matched_lines(opts, "STDIN", line_num, f)


# ##### executing main ###
if __name__ == '__main__':
    sys.exit(main())