# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

import argparse
import sys
from typing import Sequence
from fargo import __version__


def fargoArgParser(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fargo", description="Just watch shows.")
    parser.add_argument(
        "--version",
        action="version",
        version="%s" % __version__
    )

    subparsers = parser.add_subparsers(help="commands", dest="command")
    subparsers.required = True

    watch_parser = subparsers.add_parser(
        "watch",
        help="Watch a series"
    )
    add_parser = subparsers.add_parser(
        "add",
        help="Add a series alias"
    )
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a series alias"
    )
    find_parser = subparsers.add_parser(
        "find",
        help="Find torrents from https://rarbg.to"
    )

    watch_parser.add_argument(
        "alias",
        help="Alias name of the series",
        type=str,
        nargs=1
    )

    add_parser.add_argument(
        "alias",
        help="Alias name of the series",
        type=str,
        nargs=1
    )
    add_parser.add_argument(
        "dir",
        help="Directory of the series",
        type=str,
        nargs=1
    )

    delete_parser.add_argument(
        "alias",
        help="Alias name of the series",
        type=str,
        nargs=1
    )

    find_parser.add_argument(
        "name",
        help="Name of the series",
        type=str,
        nargs=1
    )

    if len(args) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args = parser.parse_args()
    if parsed_args.command == "help":
        if not parsed_args.cmd:
            parser.print_help(sys.stderr)
        else:
            try:
                subparsers.choices[parsed_args.cmd].print_help()
            except KeyError:
                print("Unknown command name %s. Type fargo -h for help." %
                      (parsed_args.cmd))
        sys.exit(1)

    return parsed_args
