# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

import os
import platform
import json
from slugify import slugify
from natsort import natsorted
from fargo import init
from fargo import opener as fop

CONFIG_DIR = os.path.join(os.path.expanduser('~'), "fargoDatabase")
CONFIG_FILE = "config.cfg"
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
CONFIG_TEMPLATE = {
    "defaultAlias": "",
    "aliasList": {},
    "defaultOpener": "",
    "webDriver": "",
    "platform": platform.system()
}
DATA_TEMPLATE = {
    "aliasName": "",
    "dir": "",
    "currEpisode": 1,
    "finished": False
}
DEFAULT_OPENER = {
    "Darwin": "IINA"
}
DATA_DIR = os.path.join(CONFIG_DIR, "data")


def checkDefaultConfigPath() -> bool:
    doInit = (not os.path.exists(CONFIG_DIR)) and (
        not os.path.exists(DATA_DIR)) and (not os.path.exists(CONFIG_PATH))
    if doInit:
        init.init()

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
        print("Directory %s created as database." % CONFIG_DIR)

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
        print("Directory %s created." % DATA_DIR)

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as cfg:
            json.dump(CONFIG_TEMPLATE, cfg)
            print("Configuration file %s created." % CONFIG_PATH)
    return True


class fargoConfigurator(object):
    def __init__(self):
        checkDefaultConfigPath()
        self.loadCfg()
        self.configPath = CONFIG_PATH
        self.currAlias = ""
        self.currAliasConfigPath = ""
        if self.configuration["defaultOpener"] == "":
            self.changeOpener(DEFAULT_OPENER[platform.system()])

    def loadCfg(self):
        with open(CONFIG_PATH, "r") as cfg:
            self.configuration = json.load(cfg)

    def saveCfg(self):
        with open(CONFIG_PATH, "w") as cfg:
            json.dump(self.configuration, cfg)

    def loadAlias(self, aliasName: str):
        with open(os.path.join(DATA_DIR, "%s.far" % aliasName), "r") as aliasCfg:
            self.currConfiguration = json.load(aliasCfg)
        self.currAlias = aliasName
        self.currAliasConfigPath = os.path.join(DATA_DIR, "%s.far" % aliasName)

    def removeAlias(self, aliasName: str):
        if self.configuration["aliasList"][aliasName] != "":
            targetDir = self.configuration["aliasList"].pop(aliasName)
            self.saveCfg()
            return targetDir
        return ""

    def saveAlias(self, aliasName: str):
        with open(os.path.join(DATA_DIR, "%s.far" % aliasName), "w") as aliasCfg:
            json.dump(self.currConfiguration, aliasCfg)
        return True

    def changeAlias(self, aliasName: str, dirPath: str) -> bool:
        if self.currAlias != "":
            self.saveAlias(self.currAlias)
        aliasSafeName = slugify(aliasName)
        aliasPath = os.path.join(DATA_DIR, "%s.far" % aliasSafeName)
        self.configuration["aliasList"][aliasName] = aliasPath
        aliasData = {}
        if not(os.path.exists(aliasPath)):
            aliasData = DATA_TEMPLATE
        else:
            with open(aliasPath, "r") as aliasCfg:
                aliasData = json.load(aliasCfg)
        aliasData["aliasName"] = aliasName
        aliasData["dir"] = dirPath
        print(aliasData["dir"])
        self.currConfiguration = aliasData
        self.currAlias = aliasSafeName
        self.configuration["aliasList"][aliasName] = aliasPath
        self.currAliasConfigPath = aliasPath
        self.saveAlias(aliasSafeName)
        self.saveCfg()

    def changeOpener(self, opener: str) -> bool:
        if (opener == "IINA"):
            self.configuration["defaultOpener"] = "IINA"
            os.system(
                "ln -s /Applications/IINA.app/Contents/MacOS/iina-cli /usr/local/bin/iina >%s" % os.path.join(CONFIG_DIR, "temp"))
            # TODO: Could raise exception
            self.saveCfg()
            return True
        else:
            print("Opener not valid")
            return False

    def getOpener(self):
        opener = self.configuration["defaultOpener"]
        if (opener == "IINA"):
            return fop.IINAOpener()
        else:
            raise fop.fileOpenerError(
                platform.system(), self.configuration["defaultOpener"])

    def getFileDir(self, aliasName: str) -> str:
        if aliasName not in self.configuration["aliasList"].keys():
            raise FileNotFoundError
        # aliasConfDir = self.configuration["aliasList"][aliasName]
        self.loadAlias(aliasName)
        targetEp = self.currConfiguration["currEpisode"]
        targetDir = self.currConfiguration["dir"]
        EPs = natsorted(os.listdir(targetDir))
        if (len(EPs) > targetEp):
            return os.path.join(targetDir, EPs[targetEp-1])
        else:
            raise IndexError

    def changeWebDriver(self, webDriverLoc: str) -> bool:
        self.configuration["webDriver"] = webDriverLoc
        self.saveCfg()
        return


checkDefaultConfigPath()
