from app import Setup
from app import Application
from app import Teardown

def main():
    setup = Setup()
    config = setup.run()

    app = Application(config)
    app.run()

    teardown = Teardown()
    teardown.run()

main()