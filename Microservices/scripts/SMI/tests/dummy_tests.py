# -*- coding: utf-8 -*-
'''

DUMMY TESTS FOR TESTER DEBUGGING
NOT INTENDED FOR ACTUAL TESTING

'''

import sys
import os
import logging
import unittest
import test_manager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


LOG = logging.getLogger(__name__)

# Leave as None to use default host
HOST_OVERRIDE = None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        HOST_OVERRIDE = sys.argv.pop()
    run_tests('DUMMY')

# HOST = HOST_OVERRIDE if HOST_OVERRIDE else test_manager.HOST
print(test_manager.HOST)
PORT = '55555'

class DummyTest(unittest.TestCase):
    """Run series of dummy tests for test format experimentation"""
    def setUp(self):
        print("")


    def test_001(self):
        """Dummy Test 1"""
        LOG.debug("DEBUG TEST 1")
        LOG.info("INFO TEST 1")
        LOG.warning("WARNING TEST 1")
        LOG.error("ERROR TEST 1")
        LOG.critical("CRITICAL TEST 1")
        self.assertTrue(5 == 5)

    def test_002(self):
        """Dummy Test 2"""
        LOG.debug("DEBUG TEST 2")
        LOG.info("INFO TEST 2")
        LOG.warning("WARNING TEST 2")
        LOG.error("ERROR TEST 2")
        LOG.critical("CRITICAL TEST 2")
        self.assertTrue(5 == 5)

    def test_003(self):
        """Dummy Test 3, check host"""
        print(HOST)

