# -*- encoding: utf-8 -*-
# fargo v1.0.0
# Just watch shows.
# Copyright © 2020, enoch2090.

from argparse import ArgumentError
from typing import Dict
from fargo.config import fargoConfigurator


def add(args: Dict[str, str]):
    aliasName = ""
    dirPath = ""
    try:
        aliasName = args["alias"][0]
        dirPath = args["dir"][0]
    except:
        raise ArgumentError(message="Argument missing")
    f = fargoConfigurator()
    f.changeAlias(aliasName=aliasName, dirPath=dirPath)
    print('Alias "%s" successfully linked to directory %s.' %
          (aliasName, dirPath))
    return
