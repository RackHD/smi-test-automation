# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

"""
Logger Toolkit
~~~~~~~~~~~~
Series of tools designed to control the logger

Copyright (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 23, 2017
"""
__title__ = 'Logger Toolkit'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import logging.config

def configure_logger_from_yaml(path):
    """Attempts to configure root logger from given YAML file"""
    import yaml
    try:
        with open(path, 'r') as stream:
            config = yaml.load(stream)
            logging.config.dictConfig(config)
    except (FileNotFoundError, yaml.YAMLError) as exc:
        print("Could not load logger configuraton from YAML file :: {}".format(exc))
