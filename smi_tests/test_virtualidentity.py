# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 4, 2017

@author: Michael Regert, Michael Hepfer
'''

import unittest
import sys
import logging
import config
from resttestms import http, json, log, test, parse

LOG = logging.getLogger(__name__)

# Leave as None to use default Host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Virtual Identity Tests")
    VirtualIdentityTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class VirtualIdentityTest(unittest.TestCase):
    """Collection of data to test the virtual identity microservice"""

    PORT = '46015'
    JSON_NAME = 'data_virtualidentity.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Delete
###################################################################################################

class Delete(VirtualIdentityTest):
    """Tests for Delete Endpoint"""

    ENDPOINT = 'delete'

    def test_json(self):
        """DELETE JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# Get
###################################################################################################

class Get(VirtualIdentityTest):
    """Tests for Get Endpoint"""

    ENDPOINT = 'get'

    def test_json(self):
        """GET JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Post
###################################################################################################

class Post(VirtualIdentityTest):
    """Tests for Post Endpoint"""

    ENDPOINT = 'post'

    def test_json(self):
        """POST JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Put
###################################################################################################

class Put(VirtualIdentityTest):
    """Tests for Put Endpoint"""

    ENDPOINT = 'put'

    def test_json(self):
        """PUT JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# Delete VirtualIdentityId
###################################################################################################

class DeleteVirtualIdentityId(VirtualIdentityTest):
    """Tests for Delete VirtualIdentityId Endpoint"""

    ENDPOINT = 'delete_virtualIdentityId'

    def test_json(self):
        """DELETE VIRTUALIDENTITYID JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# Get VirtualIdentityId
###################################################################################################

class GetVirtualIdentityId(VirtualIdentityTest):
    """Tests for Get VirtualIdentityId Endpoint"""
    ENDPOINT = 'get_virtualIdentityId'

    def test_json(self):
        """GET VIRTUALIDENTITYID JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()
