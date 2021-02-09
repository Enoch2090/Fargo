import os
import platform
import subprocess
from fargo import config


class fileOpenerError(Exception):
    def __init__(self, sys, opener):
        self.message = "Opener %s is not available on platform %s" % (
            opener, sys)


class fileOpener(object):
    def __init__(self):
        self.opener = "NULL"
        self.sys = platform.system()

    def __str__(self):
        return self.opener

    def cleanUp(self):
        print("Cleaning up")
        # TODO: Clean up


class IINAOpener(fileOpener):
    def __init__(self):
        fileOpener.__init__(self)
        self.opener = "IINA"

    def checkCompatibility(self):
        if (self.sys != "Darwin"):
            raise fileOpenerError(self.sys, self.opener)

    def open(self, fileName):
        os.system("iina '%s' >%s" %
                  (fileName, os.path.join(config.CONFIG_DIR, "temp")))
