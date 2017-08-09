# -*- coding: utf-8 -*-
"""
Server Configuration Profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on May 2, 2017
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
    LOG.info("Begin Server Configuration Profile Tests")
    SCPTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE, DEPTH_OVERRIDE)

class SCPTest(unittest.TestCase):
    """Collection of data to test the scp microservice"""

    PORT = '46018'
    JSON_NAME = 'data_scp.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override, depth_override):
        """Initialize base url, json file path, and depth"""
        cls.HOST = test.select_host(config.HOST, host_override)
        cls.DATA = test.select_directory(config.DATA, directory_override)
        cls.DEPTH = test.select_depth(config.DEPTH, depth_override)
        cls.BASE_URL = test.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = test.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Clone
###################################################################################################

class Clone(SCPTest):
    """Tests for Clone Endpoint"""

    ENDPOINT = 'clone'

    def test_json(self):
        """CLONE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Export
###################################################################################################

class Export(SCPTest):
    """Tests for Export Endpoint"""

    ENDPOINT = 'export'

    def test_induce_error(self):
        """EXPORT INDUCE ERROR TESTS"""
        test.induce_error('POST', self)

    def test_json(self):
        """EXPORT JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# ExportInventory
###################################################################################################

class ExportInventory(SCPTest):
    """Tests for ExportInventory Endpoint"""

    ENDPOINT = 'exportInventory'

    def test_json(self):
        """EXPORTINVENTORY JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Factory
###################################################################################################

class Factory(SCPTest):
    """Tests for Factory Endpoint"""

    ENDPOINT = 'factory'

    def test_json(self):
        """FACTORY JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# GetComponents
###################################################################################################

class GetComponents(SCPTest):
    """Tests for GetComponents Endpoint"""

    ENDPOINT = 'getComponents'

    def test_induce_error(self):
        """EXPORT INDUCE ERROR TESTS"""
        test.induce_error('POST', self)

    def test_json(self):
        """GETCOMPONENTS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Image Backup
###################################################################################################

class ImageBackup(SCPTest):
    """Tests for Image Backup Endpoint"""

    ENDPOINT = 'image_backup'

    def test_json(self):
        """IMAGE BACKUP JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Image Restore
###################################################################################################

class ImageRestore(SCPTest):
    """Tests for Image Restore Endpoint"""

    ENDPOINT = 'image_restore'

    def test_json(self):
        """IMAGE BACKUP JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Import
###################################################################################################

class Import(SCPTest):
    """Tests for Import Endpoint"""

    ENDPOINT = 'import'

    def test_induce_error(self):
        """EXPORT INDUCE ERROR TESTS"""
        test.run_json_test('POST', self, Export, "test_johnny_export")
        test.induce_error('POST', self)
        test.run_json_test('POST', self, Import, "test_johnny_import")

    def test_json(self):
        """IMPORT JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Lcwipe
###################################################################################################

class Lcwipe(SCPTest):
    """Tests for Lcwipe Endpoint"""

    ENDPOINT = 'lcwipe'

    def test_json(self):
        """LCWIPE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Preview
###################################################################################################

class Preview(SCPTest):
    """Tests for Preview Endpoint"""

    ENDPOINT = 'preview'

    def test_json(self):
        """PREVIEW JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Replace
###################################################################################################

class Replace(SCPTest):
    """Tests for Replace Endpoint"""

    ENDPOINT = 'replace'

    def test_json(self):
        """REPLACE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# SystemErase
###################################################################################################

class SystemErase(SCPTest):
    """Tests for SystemErase Endpoint"""

    ENDPOINT = 'systemErase'

    def test_json(self):
        """SYSTEM ERASE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# TestShare
###################################################################################################

class TestShare(SCPTest):
    """Tests for TestShare Endpoint"""

    ENDPOINT = 'testShare'

    def test_json(self):
        """TEST SHARE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# UpdateComponents
###################################################################################################

class UpdateComponents(SCPTest):
    """Tests for UpdateComponents Endpoint"""

    ENDPOINT = 'updateComponents'

    def test_induce_error(self):
        """EXPORT INDUCE ERROR TESTS"""
        test.run_json_test('POST', self, Export, "test_backup_export")
        test.induce_error('POST', self)
        test.run_json_test('POST', self, Import, "test_backup_import")

    def test_json(self):
        """UPDATECOMPONENTS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Trap ConfigureTraps TrapDestination
###################################################################################################

class TrapConfigureTrapsTrapDestination(SCPTest):
    """Tests for Trap ConfigureTraps TrapDestination Endpoint"""

    ENDPOINT = 'trap_configureTraps_trapDestination'

    def test_json(self):
        """TRAPS CONFIGURETRAPS TRAPDESTINATION JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Trap UpdateTrapFormat TrapFormat
###################################################################################################

class TrapUpdateTrapFormatFoo(SCPTest):
    """Tests for Trap UpdateTrapFormat TrapFormat Endpoint"""

    ENDPOINT = 'trap_updateTrapFormat_trapFormat'

    def test_json(self):
        """TRAPS UPDATETRAPFORMAT TRAPFORMAT JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Test Sequences
###################################################################################################

class TestSequences(SCPTest):
    """Test Sequences for SCP"""

    def test_fitfile_export_check_import(self):
        """EXPORT CHECK AND IMPORT CONFIG PROFILE"""
        test.run_json_test('POST', self, Export, "test_fitFile_export")
        test.run_json_test('POST', self, GetComponents, "test_lc_autoupdate_enabled")
        test.run_json_test('POST', self, Import, "test_fitFile_import")

    def test_johnny_export_import(self):
        """EXPORT AND IMPORT CONFIG PROFILE"""
        test.run_json_test('POST', self, Export, "test_johnny_export")
        test.run_json_test('POST', self, Import, "test_johnny_import")

    def test_update_autoupdate(self):
        """EXPORT AND IMPORT CONFIG PROFILE"""
        test.run_json_test('POST', self, Export, "test_fitFile_export")
        test.run_json_test('POST', self, GetComponents, "test_lc_autoupdate_enabled")
        test.run_json_test('POST', self, UpdateComponents, "test_autoupdate_disable")
        test.run_json_test('POST', self, GetComponents, "test_lc_autoupdate_disabled")
        test.run_json_test('POST', self, Export, "test_fitFile_export")
        test.run_json_test('POST', self, GetComponents, "test_lc_autoupdate_disabled")
        test.run_json_test('POST', self, UpdateComponents, "test_autoupdate_enable")
        test.run_json_test('POST', self, Export, "test_fitFile_export")
        test.run_json_test('POST', self, GetComponents, "test_lc_autoupdate_enabled")


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
