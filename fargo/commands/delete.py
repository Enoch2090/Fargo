# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

from argparse import ArgumentError
from typing import Dict
from fargo.config import fargoConfigurator
import os


def delete(args: Dict[str, str]):
    aliasName = ""
    try:
        aliasName = args["alias"][0]
    except:
        raise ArgumentError(message="Argument missing")
    f = fargoConfigurator()
    targetDir = ""
    try:
        targetDir = f.removeAlias(aliasName)
        os.remove(targetDir)
        print("Record file %s deleted. Alias link of %s removed." % (
            targetDir, aliasName))
    except FileNotFoundError as error:
        print(error)
        print("Alias name %s not found. Check %s" % (aliasName, f.configPath))
        return
    except OSError as error:
        print(error)
        print("Record file %s does not exist. Alias link of %s removed." % (
            targetDir, aliasName))
    return
