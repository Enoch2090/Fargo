# -*- encoding: utf-8 -*-
# fargo v1.1.0
# Just watch shows.
# Copyright © 2020, enoch2090.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from fargo import config
from typing import Dict
import pytesseract
import requests
import cv2
import os
import time
import zipfile
import stat


def downloadDriver(downloadDir, platformName, cfg):
    platformStr = platformName.replace(
        "Darwin", "mac").replace("Windows", "win").lower()
    processorBits = "64" if platformStr == "linux" or platformStr == "mac" else "32"
    chromeVersion = input(
        "Enter version of Chrome Browser, e.g. 88.0.4324.96:\n")
    url = "https://chromedriver.storage.googleapis.com/%s/chromedriver_%s%s.zip" % (
        chromeVersion, platformStr, processorBits)
    fName = "chromedriver_%s%s.zip" % (platformStr, processorBits)
    fPath = os.path.join(
        downloadDir["tempDir"], fName)
    try:
        start = time.time()
        response = requests.get(url, stream=True)
        size = 0
        chunkSize = 1024
        contentSize = int(response.headers['content-length'])
        if response.status_code == 200:
            print("Downloading %s: %s MB" %
                  (fPath, str(contentSize / chunkSize / 1024)[0:5]))
            with open(fPath, 'wb') as file:
                for data in response.iter_content(chunk_size=chunkSize):
                    file.write(data)
                    size += len(data)
                    print('\r'+'[Downloading]:%s%.2f%%' % ('>'*int(size*50 /
                                                                   contentSize), float(size / contentSize * 100)), end=' ')
        end = time.time()
        print('\nDownload completed in %.2f seconds' % (end - start))
    except Exception as e:
        print(e)
        return False
    fz = zipfile.ZipFile(os.path.join(
        downloadDir["tempDir"], fName), 'r')
    for file in fz.namelist():
        fz.extract(file, downloadDir["webDriverDir"])
        cfg.changeWebDriver(os.path.join(downloadDir["webDriverDir"], file))
        os.chmod(os.path.join(downloadDir["webDriverDir"], file), stat.S_IRWXU)
    return True


class fargoBrowser(webdriver.Chrome):
    def __init__(self):
        config_ = config.fargoConfigurator()
        dir_ = {
            "configDir": config.CONFIG_DIR,
            "webDriverDir": os.path.join(config.CONFIG_DIR, "webDrivers"),
            "tempDir": os.path.join(config.CONFIG_DIR, "tempCache")
        }
        for dirName in dir_.values():
            if not os.path.exists(dirName):
                os.mkdir(dirName)
        if config_.configuration["webDriver"] == "":
            downloadSucceeded = False
            while not downloadSucceeded:
                downloadSucceeded = downloadDriver(
                    downloadDir=dir_, platformName=config_.configuration["platform"], cfg=config_)
                if not downloadSucceeded:
                    resp = "z"
                    while resp.lower() != "y" and resp.lower() != "n":
                        resp = input("Retry downloading webdriver? [y/n]\n")
                    if resp == "n":
                        self.initStatus = False
                        return
        config_.loadCfg()
        webdriver.Chrome.__init__(
            self, executable_path=config_.configuration["webDriver"])
        self.config = config_
        self.set_window_size(1200, 800)
        self.defaultLongHoldTime = 3
        self.defaultShortHoldTime = 1
        self.dir = dir_
        self.lastUrl = ""
        self.initStatus = True
        return

    def get(self, url):
        super().get(url)
        self.lastUrl = url
        self.checkAvaliability()

    def hold(self, holdTime):
        time.sleep(holdTime)
        self.refreshUrl()

    def checkAvaliability(self):
        if "threat_defence.php?defence=1" in self.current_url:
            self.hold(1)
            self.checkAvaliability()
        elif "threat_defence.php?defence=2" in self.current_url:
            self.solveCaptcha()
        elif "threat_defence.php?defence=no" in self.current_url:
            # self.reloadLast()
            return
        else:
            return

    def solveCaptcha(self):
        imgTemp = os.path.join(self.dir["tempDir"], "captchaTemp.png")
        self.get_screenshot_as_file(imgTemp)
        capcha = self.find_element_by_css_selector(
            "body > form > div > div > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2) > img")
        left = int(capcha.location['x'])
        top = int(capcha.location['y'])
        right = int(capcha.location['x'] + capcha.size['width'])
        bottom = int(capcha.location['y'] + capcha.size['height'])
        #print(left, top, right, bottom)
        img = cv2.cvtColor(cv2.imread(imgTemp), cv2.COLOR_BGR2GRAY)
        img_cropped = img[top:bottom, left:right]
        solution = pytesseract.image_to_string(img_cropped)
        inputbox = self.find_element_by_css_selector("#solve_string")
        inputbox.send_keys(solution, Keys.ENTER)
        os.remove(imgTemp)
        self.hold(self.defaultLongHoldTime)
        return

    def refreshUrl(self):
        self.lastUrl = self.current_url

    def reloadLast(self):
        self.get(self.lastUrl)
        return

    def searchShow(self, name):
        searchbox = self.find_element_by_css_selector("#searchinput")
        searchbox.send_keys(name, Keys.ENTER)
        self.hold(self.defaultLongHoldTime)
        return

    def getSearchTable(self):
        try:
            resultTable = self.find_element_by_css_selector(
                "body > table:nth-child(6) > tbody > tr > td:nth-child(2) > div > table > tbody > tr:nth-child(2) > td > table.lista2t")
            tableTdList = resultTable.find_elements(By.TAG_NAME, "tr")
            linkDict = {}
            for td in tableTdList:
                linkList = td.find_elements_by_xpath(".//td")
                if len(linkList) == 0:
                    continue
                print(linkList[1].find_elements_by_xpath(
                    ".//a")[0].get_attribute("title"), " - ", linkList[1].find_elements_by_xpath(
                    ".//a")[0].get_attribute("href"))
            # print(tableTdList)
        except Exception as e:
            print(e)
            return


def find(args: Dict[str, str]):
    print("Note that this feature is highly unstable. If rarbg.to rejects your access, please try again later or use another IP address.")
    showName = args["name"][0]
    url = "http://rarbgproxy.org/torrents.php?r=74830847"
    fb = fargoBrowser()
    if fb.initStatus == False:
        print("Initialization of Selenium webdrive failed.")
        return
    fb.get(url)
    fb.searchShow("%s" % (showName))
    fb.getSearchTable()
    fb.close()
