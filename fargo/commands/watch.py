# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

from argparse import ArgumentError
from typing import Dict
from fargo.config import fargoConfigurator
from fargo.opener import fileOpener
from fargo.opener import fileOpenerError


def watch(args: Dict[str, str]):
    aliasName = ""
    dirPath = ""
    try:
        aliasName = args["alias"][0]
    except:
        raise ArgumentError(message="Argument missing")
    f = fargoConfigurator()
    targetDir = ""

    try:
        targetDir = f.getFileDir(aliasName)
    except FileNotFoundError:
        print("Alias name %s not found. Check %s" % (aliasName, f.configPath))
        return
    except IndexError:
        print("Episode not found. Check %s" % (f.currAliasConfigPath))
        return

    try:
        o = f.getOpener()

    except fileOpenerError:
        print(fileOpenerError.message)
        return

    print(targetDir)
    o.open(targetDir)
    response = "z"
    while (response != "y" and response != "n"):
        response = input(
            "Have you finished this episode? [y/n]: \n").lower()[0]

    if response == "y":
        print("%s ep%s finished!" %
              (aliasName, f.currConfiguration["currEpisode"]))
        f.currConfiguration["currEpisode"] += 1
        f.saveAlias(aliasName)
    else:
        print("Sure.")

    return
