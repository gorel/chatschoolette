import os
import unittest

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = BASE_DIR + '/tests'

loader = unittest.TestLoader()
runner = unittest.TextTestRunner()

suite = loader.discover(TEST_DIR)
runner.run(suite)
