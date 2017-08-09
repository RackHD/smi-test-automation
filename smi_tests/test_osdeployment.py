# -*- coding: utf-8 -*-
"""
OS Deployment
~~~~~~~~~~~~~

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on August 9, 2017
"""

import unittest
import sys
import logging
import config
from resttestms import http, json, log, test, parse

LOG = logging.getLogger(__name__)

# Leave as None to use default host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

# Leave as None to use default depth
DEPTH_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin OS Deployment Tests")
    OSDeploymentTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE, DEPTH_OVERRIDE)

class OSDeploymentTest(unittest.TestCase):
    """Collection of data to test the os deployment microservice"""

    PORT = '46014'
    JSON_NAME = 'data_osdeployment.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override, depth_override):
        """Initialize base url, json file path, and depth"""
        cls.HOST = test.select_host(config.HOST, host_override)
        cls.DATA = test.select_directory(config.DATA, directory_override)
        cls.DEPTH = test.select_depth(config.DEPTH, depth_override)
        cls.BASE_URL = test.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = test.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Deploy
###################################################################################################

class Deploy(OSDeploymentTest):
    """Tests for Deploy Endpoint"""

    ENDPOINT = 'deploy'

    def test_json(self):
        """DEPLOY JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Iso Create
###################################################################################################

class IsoCreate(OSDeploymentTest):
    """Tests for Iso Create Endpoint"""

    ENDPOINT = 'iso_create'

    def test_json(self):
        """ISO CREATE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Version
###################################################################################################

class Version(OSDeploymentTest):
    """Tests for Version Endpoint"""

    ENDPOINT = 'version'

    def test_json(self):
        """VERSION JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Test Sequences
###################################################################################################

class TestSequences(OSDeploymentTest):
    """Test Sequences for OS Deployment"""

    def test_placeholder(self):
        """EXPORT CHECK AND IMPORT CONFIG PROFILE"""
        # test.run_json_test('POST', self, Export, "test_fitFile_export")
        pass

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA, DEPTH = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    DEPTH_OVERRIDE = DEPTH if DEPTH else DEPTH_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()
