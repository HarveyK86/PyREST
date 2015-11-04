import re
import requests

from welcome import welcome

class Setup(object):

    __filename = "app.properties"
    __regex = r"^([^#][\w\.]*)=(.*)$"
    __keys = ("url.host", "url.route", "url.params", "user.username", "user.password")
    __required = ("url.host")

    def __init__(self):
        #print("Setup : __init__")
        pass

    def run(self):
        print("Setup : run")

        config = self.__getConfig()

        print("Setup : run[returns=" + str(config) + "]")
        return config

    def __getConfig(self):
        print("Setup : __getConfig")

        file = open(self.__filename)
        lines = file.readlines()
        config = {}

        for line in lines:
            match = re.search(self.__regex, line)
            if match: config[match.group(1)] = match.group(2)

        print("----- Configuration -----")

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

        print("-------------------------")

        print("Setup : __getConfig[returns=" + str(config) + "]")
        return config

class Application(object):

    __urlFormat1 = "{host}{route}"
    __urlFormat2 = "{urlFormat1}?{params}"

    def __init__(self, config):
        print("Application : __init__[config=" + str(config) + "]")

        self.__config = config

    def run(self):
        print("Application : run")

        welcome()

        url = self.__getURL()

        print("Application : run : URL is " + url)

        response = requests.get(url)
        print(response)

    def __getURL(self):
        #print("Application : __getURL")

        urlFormat1 = self.__urlFormat1.format(host = self.__config["url.host"], route = self.__config["url.route"])

        if self.__config.get("url.params"):
            url = self.__urlFormat2.format(urlFormat1 = urlFormat1, params = self.__config["url.params"])
        else:
            url = urlFormat1

        print("Application : __getURL[returns=" + url + "]")
        return url

class Teardown(object):

    def __init__(self):
        #print("Teardown : __init__")
        pass

    def run(self):
        #print("Teardown : run")
        pass