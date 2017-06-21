# -*- coding: utf-8 -*-

'''
SMI-TEST-AUTOMATION
~~~~~~~~~~~~~~~~~~~

Run tests on the specified microservices.
Tests run in no particular order.

Alias Reference
DISC:1 FWUP:2 CHIN:3 SVIN:4 PWTH:5 SCP:6 VID:7 VNW:8

Microservice IDs can be separated with or without a space
Microservice Aliases are case insensitive
Aliases and IDs can be passed as parameters in any order

Argument format examples:

>>> run_tests - Run All Tests
>>> run_tests 4 - Run Test With ID 4
>>> run_tests 8451825 - Run Tests With ID 8, 4, 1, 2, and 5
>>> run_tests SVIN - Run Test With ID 4
>>> run_tests DISC SCP CHIN - Run Tests with ID 1, 6, and 3
>>> run_tests 24 vNw 314 ScP - Run Tests with ID 2, 4, 8, 3, and 6

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.

Created on June 20, 2017

'''
__title__ = 'run_tests'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import sys
import unittest

from discoveryTest import DiscoveryMicroserviceTest as disc
from firmwareUpdateTest import FirmwareUpdateTest as fwup
from chassisInventoryTest import ChassisInventoryMicroserviceTest as chin
from serverInventoryTest import ServerInventoryMicroserviceTest as svin
from powerThermalTest import PowerThermalMicroserviceTest as pwth
from scpTest import SCPMicroserviceTest as scp
from virtualIdentityTest import VirtualIdentityTest as vid
from virtualNetworkTest import VirtualNetworkTest as vnw

# ----- ARGUMENT CONFIGURATION PROFILE -----
##############################################

# Microservice ID
ID = {
    # Device Discovery
    disc : 1,
    # Server Firmware Update
    fwup : 2,
    # Chassis Inventory
    chin : 3,
    # Server Inventory
    svin : 4,
    # Power Thermal Monitoring
    pwth : 5,
    # Server Configuration Profile
    scp : 6,
    # Virtual Identity
    vid : 7,
    # Virtual Network
    vnw : 8
}
# Microservice Alias
ALIAS = {
    'DISC' : ID[disc],
    'FWUP' : ID[fwup],
    'CHIN' : ID[chin],
    'SVIN' : ID[svin],
    'PWTH' : ID[pwth],
    'SCP' : ID[scp],
    'VID' : ID[vid],
    'VNW' : ID[vnw],
}

##############################################

def _generate_test_keys(arguments):
    "Parse data from arguments to determine which tests will be loaded"

    # Default to returning keys for all tests
    if not arguments:
        return {n for n in range(1, 9)}

    test_keys = set()

    def _add_key_from_id(number):
        for digit in str(number):
            key_num = int(digit)
            if 1 <= key_num <= 8:
                test_keys.add(key_num)
            else:
                raise ValueError('Invalid Microservice ID - {}'.format(key_num))

    def _add_key_from_alias(key_alias):
        key_alias = key_alias.upper()
        if key_alias in ALIAS:
            test_keys.add(ALIAS[key_alias])
        else:
            raise ValueError('Invalid Microservice Alias - {}'.format(key_alias))

    for arg in arguments:
        if str(arg).isdecimal():
            _add_key_from_id(arg)
        elif arg.isalpha():
            _add_key_from_alias(arg)
        else:
            raise ValueError('Invalid Argument - {}'.format(str(arg)))

    return test_keys

def _load_tests(test_keys):
    "Load tests into suite for each of the test keys passed in"
    test_suite = []
    service_dict = {service_id: service for service, service_id in ID.items()}
    for key in test_keys:
        test_suite.append(unittest.TestLoader().loadTestsFromTestCase(service_dict[key]))
    return unittest.TestSuite(test_suite)

def run_tests(*args):
    "Run specified tests using arguments"
    arguments = [arg for arg in args]
    # logger.info("Arguments - {}".format(arguments))
    keys = _generate_test_keys(arguments)
    # logger.info("Generated Keys - {}".format(keys))
    test_suite = _load_tests(keys)
    # logger.debug("Loaded Tests - {}".format(test_suite))
    unittest.TextTestRunner(verbosity=2).run(test_suite)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
