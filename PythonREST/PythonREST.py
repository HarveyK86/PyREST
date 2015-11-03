import re

class Application:

    filename = "PythonREST.config"
    regex = r"^([\w.]*)=(.*)$"
    keys = ("url.host", "url.route", "url.params")
    config = {}

    def __init__(self):
        print("Application : __init__")

        file = open(self.filename)
        lines = file.readlines()

        for line in lines:
            match = re.search(self.regex, line)

            if match:
                self.config[match.group(1)] = match.group(2)
            else:
                print("Application : __init__ : no default config")

        for key in self.keys:
            if self.config.get(key):
                value = input("Enter " + key + " (default: " + self.config[key] + ") >> ")
                if not value: value = self.config[key]
            else:
                value = input("Enter " + key + " >> ")

            if value:
                self.config[key] = value
            else:
                raise RuntimeError("Value for " + key + " required!")

    def run(self):
        print("Application : run : config=" + str(self.config))