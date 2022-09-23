#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import regular expression library.
import re
# Import configparser library.
import configparser
#
#
#
class DialogParser(configparser.ConfigParser):

    """
        Modified ConfigParser that allow ':' in keys and only '=' as separator.
    """

    OPTCRE = re.compile(
        r'(?P<option>[^=\s][^=]*)'          # allow only = 
        r'\s*(?P<vi>[=])\s*'                # for option separator           
        r'(?P<value>.*)$'                   
    )

    def __init__(self):

        """ Class constructor. """
            
        # Init parent class Domain allowing no value.
        super().__init__(allow_no_value=True)
