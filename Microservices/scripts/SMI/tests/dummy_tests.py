# -*- coding: utf-8 -*-
'''

DUMMY TESTS FOR LOGGER CONFIGURATION
NOT INTENDED FOR ACTUAL TESTING

'''
import json
import unittest
import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

logger.debug("OUTSIDE CLASS DEBUG TEST")
logger.info("OUTSIDE CLASS INFO TEST")
logger.warning("OUTSIDE CLASS WARNING TEST")
logger.error("OUTSIDE CLASS ERROR TEST")
logger.critical("OUTSIDE CLASS CRITICAL TEST")

class DummyMicroserviceTest(unittest.TestCase):    

    def test_001(self): 
        print("")       
        logger.debug("DEBUG TEST 1")
        logger.info("INFO TEST 1")
        logger.warning("WARNING TEST 1")
        logger.error("ERROR TEST 1")
        logger.critical("CRITICAL TEST 1")

    def test_002(self):
        print("")   
        logger.debug("DEBUG TEST 2")
        logger.info("INFO TEST 2")
        logger.warning("WARNING TEST 2")
        logger.error("ERROR TEST 2")
        logger.critical("CRITICAL TEST 2")   


if __name__=="__main__":
    if len(sys.argv) > 1:
        host = sys.argv.pop()
    else:
        host = "http://localhost:46019"
    from run_tests import run_tests
    run_tests('DUMMY')

    