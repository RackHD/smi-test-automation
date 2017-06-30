# -*- coding: utf-8 -*-
"""
Logger Toolkit
~~~~~~~~~~~~
Series of tools designed to control the logger

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 23, 2017
"""

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

def exception(logger):
    """
    Return decorator to log exceptions using the specified logger
    """
    def decorator(func):
        """Decorate function with a try catch and a log record"""
        def wrapper(*args, **kwargs):
            """Wraps around each test case"""
            try:
                return func(*args, **kwargs)
            except:
                logger.exception("Exception in %s", func.__name__)
                raise
        return wrapper
    return decorator
