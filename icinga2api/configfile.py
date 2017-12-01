# -*- coding: utf-8 -*-
'''
Icinga 2 API client config file
'''

import os
import sys
# pylint: disable=import-error,no-name-in-module
if sys.version_info >= (3, 0):
    import configparser as configparser
else:
    import ConfigParser as configparser
# pylint: enable=import-error,no-name-in-module

from icinga2api.exceptions import Icinga2ApiConfigFileException


class ClientConfigFile(object):
    '''
    Icinga 2 API config file
    '''

    def __init__(self, file_name):
        '''
        initialization
        '''

        self.file_name = file_name
        self.section = 'api'
        self.url = None
        self.username = None
        self.password = None
        self.certificate = None
        self.key = None
        self.ca_certificate = None
        self.timeout = None
        if self.file_name:
            self.check_access()

    def check_access(self):
        '''
        check access to the config file

        :returns: True
        :rtype: bool
        '''

        if not os.path.exists(self.file_name):
            raise Icinga2ApiConfigFileException(
                'Config file "{0}" doesn\'t exist.'.format(
                    self.file_name
                )
            )

        if not os.access(self.file_name, os.R_OK):
            raise Icinga2ApiConfigFileException(
                'No read access for config file "{0}".\n'.format(
                    self.file_name
                )
            )

        return True

    def parse(self):
        '''
        parse the config file
        '''

        cfg = configparser.ConfigParser()
        cfg.read(self.file_name)

        if not cfg.has_section(self.section):
            raise Icinga2ApiConfigFileException(
                'Config file is missing "{0}" section.'.format(
                    self.section
                )
            )

        # [api]/url
        try:
            self.url = str(cfg.get(
                self.section,
                'url'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/username
        try:
            self.username = str(cfg.get(
                self.section,
                'username'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/password
        # do we really want to store the password here
        # or use the keyring
        try:
            self.password = str(cfg.get(
                self.section,
                'password'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/certificate
        try:
            self.certificate = str(cfg.get(
                self.section,
                'certificate'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/client_key
        try:
            self.key = str(cfg.get(
                self.section,
                'key'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/ca_certificate
        try:
            self.ca_certificate = str(cfg.get(
                self.section,
                'ca_certificate'
            )).strip()
        except configparser.NoOptionError:
            pass

        # [api]/timeout
        try:
            self.timeout = str(cfg.get(
                self.section,
                'timeout'
            )).strip()
        except configparser.NoOptionError:
            pass
