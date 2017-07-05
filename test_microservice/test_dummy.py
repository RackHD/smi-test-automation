# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import unittest
import sys
import logging
from toolkit import http, json, log, test

LOG = logging.getLogger(__name__)
# Leave as None to use default Host
HOST_OVERRIDE = 'httpbin.org'
# Leave as None to use default json directory
DIRECTORY_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Firmware Update Tests")
    FirmwareUpdateTest.initialize_data(HOST_OVERRIDE, DIRECTORY_OVERRIDE)

class FirmwareUpdateTest(unittest.TestCase):
    """Collection of data to test the firmware update microservice"""

    HOST = 'localhost' # will grab default from elsewhere
    PORT = '80'
    DIRECTORY = 'request_data' # will grab default from elsewhere
    JSON_NAME = 'request_dummy.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(cls.HOST, host_override)
        cls.DIRECTORY = json.select_directory(cls.DIRECTORY, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DIRECTORY, cls.JSON_NAME)

###################################################################################################
# Version
###################################################################################################

class Tomato(FirmwareUpdateTest):
    """Tests for Version Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'tomato'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)
    
    @unittest.skip("")
    @log.exception(LOG)
    def test_bad_params(self):
        """Make a request to downloader with missing or empty data, check for failure"""
        test.get_bad_data(self)
    
    @log.exception(LOG)
    def test_json(self):
        """Run tests specified in JSON"""
        test.get_json(self)

if __name__ == "__main__":
    ARGS = sys.argv[1:].copy()
    if ARGS:
        HOST_OVERRIDE = ARGS.pop(0)
        LOG.info("Host Override : %s", HOST_OVERRIDE)
        sys.argv.pop()
        if ARGS:
            DIRECTORY_OVERRIDE = ARGS.pop(0)
            LOG.info("Directory Override : %s", DIRECTORY_OVERRIDE)
            sys.argv.pop()

    log.configure_logger_from_yaml('../logs/logger_config.yml')
    unittest.main()
