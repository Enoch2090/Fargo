# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

import sys
from fargo.argParser import fargoArgParser
from fargo.commands.add import add
from fargo.commands.watch import watch
from fargo.commands.delete import delete
from fargo.commands.find import find

COMMANDS = {
    "add": add,
    "watch": watch,
    "delete": delete,
    "find": find
}


def dispatch(function, *args, **kwargs):
    """
    Dispatch command line action to proper
    kb function
    """
    return COMMANDS[function](*args, **kwargs)


def main():
    args = fargoArgParser(sys.argv[1:])
    cmd = args.command
    cmd_params = vars(args)
    try:
        dispatch(cmd, cmd_params)
    except KeyError as error:
        print(error)
        print("Command %s is not valid." % cmd)
