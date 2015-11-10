import logging
import re
import requests

from welcome import welcome

class Setup(object):

    __filename = "app.properties"
    __regex = r"^([^#][\w\.-]*)=(.*)$"
    __keys = ("request.type", "request.content-list", "url.host", "url.route", "url.params", "user.username", "user.password")
    __required = ("request.type", "url.host")

    __logger = logging.getLogger("PyREST")

    def __init__(self):
        #print("Setup : __init__")

        fileHandler = logging.FileHandler("output.log")
        consoleHandler = logging.StreamHandler()

        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(fileHandler)
        self.__logger.addHandler(consoleHandler)

    def run(self):
        self.__logger.info("Setup : run")

        config = self.__getConfig()

        self.__logger.info("Setup : run[returns=" + str(config) + "]")
        return config

    def __getConfig(self):
        self.__logger.info("Setup : __getConfig")

        file = open(self.__filename)
        lines = file.readlines()
        config = {}

        for line in lines:
            match = re.search(self.__regex, line)
            if match: config[match.group(1)] = match.group(2)

        self.__logger.info("----- Configuration -----")

        for key in self.__keys:
            if config.get(key):
                value = input("Enter " + key + " (default: " + config[key] + ") >> ")
                if not value: value = config[key]
            else:
                value = input("Enter " + key + " >> ")

            if value:
                config[key] = value
            elif key in self.__required:
                raise RuntimeError("Value for " + key + " required!")
            else:
                config[key] = ""

        self.__logger.info("-------------------------")

        self.__logger.info("Setup : __getConfig[returns=" + str(config) + "]")
        return config

class Application(object):

    __urlFormat1 = "{host}{route}"
    __urlFormat2 = "{urlFormat1}?{params}"

    __logger = logging.getLogger("PyREST")

    def __init__(self, config):
        self.__logger.info("Application : __init__[config=" + str(config) + "]")

        self.__config = config

    def run(self):
        self.__logger.info("Application : run")

        welcome()

        url = self.__getURL()
        contentList = self.__getContentList()

        if self.__config["request.type"] == "GET":
            response = self.__httpGet(url)

        elif self.__config["request.type"] == "POST":

            for content in contentList:
                response = self.__httpPost(url, content)

        self.__logger.info("Application : run : response is 200: '" + response.text + "'")

    def __getURL(self):
        #self.__logger.info("Application : __getURL")

        urlFormat1 = self.__urlFormat1.format(host = self.__config["url.host"], route = self.__config["url.route"])

        if self.__config.get("url.params"):
            url = self.__urlFormat2.format(urlFormat1 = urlFormat1, params = self.__config["url.params"])
        else:
            url = urlFormat1

        self.__logger.info("Application : __getURL[returns=" + url + "]")
        return url

    def __getContentList(self):
        #self.__logger.info("Application : __getContentList")

        filename = self.__config.get("request.content-list")
        contentList = []

        if filename:
            file = open(filename)
            lines = file.readlines()

            for line in lines:
                content = line.replace("\n", "")
                contentList.append(content)

        self.__logger.info("Application : __getContentList[returns=" + str(contentList) + "]")
        return contentList

    def __httpGet(self, url):
        self.__logger.info("Application : __httpGet[url=" + url + "]")

        response = requests.get(url)

        self.__logger.info("Application : __httpGet[url=" + url + ", returns=" + str(response) + "]")
        return response

    def __httpPost(self, url, content):
        self.__logger.info("Application : __httpPost[url=" + url + ", content=" + content + "]")

        response = requests.post(url, auth=(self.__config["user.username"], self.__config["user.password"]), data=content)

        self.__logger.info("Application : __httpPost[url=" + url + ", content=" + content + ", returns=" + str(response) + "]")
        return response

class Teardown(object):

    __logger = logging.getLogger("PyREST")

    def __init__(self):
        #self.__logger.info("Teardown : __init__")
        pass

    def run(self):
        #self.__logger.info("Teardown : run")
        pass