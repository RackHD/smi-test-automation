# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

"""
JSON Toolkit
~~~~~~~~~~~~
Series of tools designed around JSON

Copyright (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 26, 2017
"""
__title__ = 'jsontools'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import logging
import json

LOG = logging.getLogger(__name__)


def load_test_data(directory, task):
    """Load test data from provided json file"""
    with open(directory) as stream:
        data = json.load(stream)
        url = data["services"][task]["url"]
        parameters = data["services"][task]["parameters"]
        payload = data["services"][task]["payload"]
        return url, parameters, payload
