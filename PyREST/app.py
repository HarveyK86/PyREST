import re

from welcome import welcome

class Setup(object):

    __filename = "app.properties"
    __regex = r"^([\w-]*):(.*)$"
    __keys = ("url-host", "url-route", "url-params")

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

            if match:
                config[match.group(1)] = match.group(2)
            else:
                print("Setup : __getConfig : no default config")

        print("----- Configuration -----")

        for key in self.__keys:
            if config.get(key):
                value = input("Enter " + key + " (default: " + config[key] + ") >> ")
                if not value: value = config[key]
            else:
                value = input("Enter " + key + " >> ")

            if value:
                config[key] = value
            else:
                raise RuntimeError("Value for " + key + " required!")

        print("-------------------------")

        print("Setup : __getConfig[returns=" + str(config) + "]")
        return config

class Application(object):

    __format = "{url-host}{url-route}?{url-params}"

    def __init__(self, config):
        print("Application : __init__[config=" + str(config) + "]")

        self.__config = config

    def run(self):
        print("Application : run")

        welcome()

        url = self.__getURL()
        print("Application : run : URL is " + url)

    def __getURL(self):
        #print("Application : __getURL")

        url = self.__format.format(**self.__config)

        print("Application : __getURL[returns=" + url + "]")
        return url

class Teardown(object):

    def __init__(self):
        #print("Teardown : __init__")
        pass

    def run(self):
        #print("Teardown : run")
        pass