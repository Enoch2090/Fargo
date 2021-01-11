import os
import platform
import subprocess
from fargo.config import CONFIG_DIR


class fileOpenerError(Exception):
    def __init__(self, sys, opener):
        self.message = "Opener %s is not available on platform %s" % (
            opener, sys)


class fileOpener(object):
    def __init__(self, opener="IINA"):
        self.opener = opener
        self.sys = platform.system()

    def __str__(self):
        return self.opener

    def setOpener(self, opener):
        self.opener = opener

    def checkCompatibility(self):
        if (self.sys != "Darwin" and self.opener == "IINA"):
            raise fileOpenerError(self.sys, self.opener)

    def open(self, fileName):
        if (self.opener == "IINA"):
            os.system(
                "ln -s /Applications/IINA.app/Contents/MacOS/iina-cli /usr/local/bin/iina >%s" % os.path.join(CONFIG_DIR, "temp"))
            os.system("iina '%s' >%s" %
                      (fileName, os.path.join(CONFIG_DIR, "temp")))
