import re

class Setup(object):

    __filename = "app.properties"
    __regex = r"^([\w.-]*):(.*)$"
    __keys = ("url.host", "url.route", "url.params")

    def __init__(self):
        print("Setup : __init__")

    def run(self):
        print("Setup : run")

        file = open(self.__filename)
        lines = file.readlines()
        config = {}

        for line in lines:
            match = re.search(self.__regex, line)

            if match:
                config[match.group(1)] = match.group(2)
            else:
                print("Setup : run : no default config")

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

        return config

class Application(object):

    def __init__(self):
        print("Application : __init__")

    def run(self, config):
        print("Application : run[config=" + str(config) + "]")

class Teardown(object):

    def __init__(self):
        print("Teardown : __init__")

    def run(self):
        print("Teardown : run")