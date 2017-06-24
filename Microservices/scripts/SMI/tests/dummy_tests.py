# -*- coding: utf-8 -*-
'''

DUMMY TESTS FOR TESTER DEBUGGING
NOT INTENDED FOR ACTUAL TESTING

'''

import sys
import os
import logging
import unittest
from toolkit import httptools

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get default logger
LOG = logging.getLogger(__name__)

class DummyTest(unittest.TestCase):
    """Run series of dummy tests for test format experimentation"""

    # Change to override HOST, None is defaut
    host = None

    @classmethod
    def run_with_host(cls, default_host):
        """Run tests using data provided"""
        cls.host = httptools.select_host(default_host, cls.host)
        unittest.main()

    def setUp(self):
        print("")

    def test_001(self):
        """Dummy Test 1, Logger Test"""
        LOG.warning("WARNING TEST 1")
        LOG.error("ERROR TEST 1")
        LOG.critical("CRITICAL TEST 1")
        self.assertTrue(5 == 5)

    def test_002(self):
        """Dummy Test 2, Logger Test"""
        LOG.debug("DEBUG TEST 2")
        LOG.info("INFO TEST 2")
        self.assertTrue(5 == 5)

    def test_003(self):
        """Dummy Test 3, check host"""
        print("HOST: {}".format(self.host))

    def test_004(self):
        """Dummy Test 4, check default host"""
        print("DEFAULT HOST: {}".format(self.host))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        HOST = sys.argv.pop()
        DummyTest.run_with_data(HOST)
    else:
        import test_manager
        test_manager.run_tests('DUMMY')

