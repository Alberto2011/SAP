# -*- coding: utf-8 -*-
"""Setup the SAP1 application"""

import logging

from sap1.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)

from schema import setup_schema
from bootstrap import bootstrap

def setup_app(command, conf, vars):
    """Place any commands to setup sap1 here"""
    load_environment(conf.global_conf, conf.local_conf)
    setup_schema(command, conf, vars)
    bootstrap(command, conf, vars)
