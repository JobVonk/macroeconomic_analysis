from tests.tests_unit import TestsUnit
import logging
import sys


root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def main_tests():
    unit_tests = TestsUnit()
    unit_tests.setup_method()
    unit_tests.run()

if __name__ == "__main__":
    main_tests()    