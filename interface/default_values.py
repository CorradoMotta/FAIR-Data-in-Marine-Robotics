# -*- coding: utf-8 -*-
"""
==============
default_values
==============

Author:         Corrado Motta   
Date:           11/2021

This module contains a class where all default values are stored, to be used by the 
interface to populate the global attributes.

"""

import os
from os import path
from os.path import dirname, abspath
import sys
import configparser

class default_ini:

    def __init__(self, file_path):

        self.file_path = file_path
        self.default_dict = {}

    def read_default(self):

        read_config = configparser.ConfigParser()
        read_config.read(self.file_path)

        if(read_config.has_section("default_values")):
            auto_dict = dict(read_config.items('default_values'))
            # remove empty values, if any
            self.default_dict={k: v for k, v in auto_dict.items() if v}
