# -*- coding: utf-8 -*-
'''
Icinga 2 API objects
'''

from __future__ import print_function
import logging

from icinga2api.base import Base
from icinga2api.exceptions import Icinga2ApiException

LOG = logging.getLogger(__name__)


class Objects(Base):
    '''
    Icinga 2 API objects class
    '''

    base_url_path = 'v1/objects'

    @staticmethod
    def _convert_object_type(object_type=None):
        '''
        check if the object_type is a valid Icinga 2 object type
        '''

        type_conv = {
            'ApiListener': 'apilisteners',
            'ApiUser': 'apiusers',
            'CheckCommand': 'checkcommands',
            'Arguments': 'argumentss',
            'CheckerComponent': 'checkercomponents',
            'CheckResultReader': 'checkresultreaders',
            'Comment': 'comments',
            'CompatLogger': 'compatloggers',
            'Dependency': 'dependencys',
            'Downtime': 'downtimes',
            'Endpoint': 'endpoints',
            'EventCommand': 'eventcommands',
            'ExternalCommandListener': 'externalcommandlisteners',
            'FileLogger': 'fileloggers',
            'GelfWriter': 'gelfwriters',
            'GraphiteWriter': 'graphitewriters',
            'Host': 'hosts',
            'HostGroup': 'hostgroups',
            'IcingaApplication': 'icingaapplications',
            'IdoMySqlConnection': 'idomysqlconnections',
            'IdoPgSqlConnection': 'idopgsqlconnections',
            'LiveStatusListener': 'livestatuslisteners',
            'Notification': 'notifications',
            'NotificationCommand': 'notificationcommands',
            'NotificationComponent': 'notificationcomponents',
            'OpenTsdbWriter': 'opentsdbwriters',
            'PerfdataWriter': 'perfdatawriters',
            'ScheduledDowntime': 'scheduleddowntimes',
            'Service': 'services',
            'ServiceGroup': 'servicegroups',
            'StatusDataWriter': 'statusdatawriters',
            'SyslogLogger': 'syslogloggers',
            'TimePeriod': 'timeperiods',
            'User': 'users',
            'UserGroup': 'usergroups',
            'Zone': 'zones',
        }
        if object_type not in type_conv:
            raise Icinga2ApiException(
                'Icinga 2 object type "{}" does not exist.'.format(
                    object_type
                ))

        return type_conv[object_type]

    def get(self,
            object_type,
            name,
            attrs=None,
            joins=None):
        '''
        get object by type or name

        :param object_type: type of the object
        :type object_type: string
        :param name: list object with this name
        :type name: string
        :param attrs: only return these attributes
        :type attrs: list
        :param joins: show joined object
        :type joins: list

        example 1:
        get('Host', 'webserver01.domain')

        example 2:
        get('Service', 'webserver01.domain!ping4')

        example 3:
        get('Host', 'webserver01.domain', attrs=["address", "state"])

        example 4:
        get('Service', 'webserver01.domain!ping4', joins=True)
        '''

        return self.list(object_type, name, attrs, joins=joins)[0]

    def list(self,
             object_type,
             name=None,
             attrs=None,
             filter=None,
             filter_vars=None,
             joins=None):
        '''
        get object by type or name

        :param object_type: type of the object
        :type object_type: string
        :param name: list object with this name
        :type name: string
        :param attrs: only return these attributes
        :type attrs: list
        :param filter: filter the object list
        :type filter: string
        :param filter_vars: variables used in the filter expression
        :type filter_vars: dict
        :param joins: show joined object
        :type joins: list

        example 1:
        list('Host')

        example 2:
        list('Service', 'webserver01.domain!ping4')

        example 3:
        list('Host', attrs='["address", "state"])

        example 4:
        list('Host', filter='match("webserver*", host.name)')

        example 5:
        list('Service', joins=['host.name'])

        example 6:
        list('Service', joins=True)
        '''

        object_type_url_path = self._convert_object_type(object_type)
        url_path = '{}/{}'.format(self.base_url_path, object_type_url_path)
        if name:
            url_path += '/{}'.format(name)

        payload = {}
        if attrs:
            payload['attrs'] = attrs
        if filter:
            payload['filter'] = filter
        if filter_vars:
            payload['filter_vars'] = filter_vars
        if isinstance(joins, bool) and joins:
            payload['all_joins'] = '1'
        elif joins:
            payload['joins'] = joins

        return self._request('GET', url_path, payload)['results']

    def create(self,
               object_type,
               name,
               templates=None,
               attrs=None):
        '''
        create an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param templates: templates used
        :type templates: list
        :param attrs: object's attributes
        :type attrs: dictionary

        example 1:
        create('Host', 'localhost', ['generic-host'], {'address': '127.0.0.1'})

        example 2:
        create('Service',
               'testhost3!dummy',
               {'check_command': 'dummy'},
               ['generic-service'])
        '''

        object_type_url_path = self._convert_object_type(object_type)

        payload = {}
        if attrs:
            payload['attrs'] = attrs
        if templates:
            payload['templates'] = templates

        url_path = '{}/{}/{}'.format(
            self.base_url_path,
            object_type_url_path,
            name
        )

        return self._request('PUT', url_path, payload)

    def update(self,
               object_type,
               name,
               attrs):
        '''
        update an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param attrs: object's attributes to change
        :type attrs: dictionary

        example 1:
        update('Host', 'localhost', {'address': '127.0.1.1'})

        example 2:
        update('Service', 'testhost3!dummy', {'check_interval': '10m'})
        '''
        object_type_url_path = self._convert_object_type(object_type)
        url_path = '{}/{}/{}'.format(
            self.base_url_path,
            object_type_url_path,
            name
        )

        return self._request('POST', url_path, attrs)

    def delete(self,
               object_type,
               name=None,
               filter=None,
               filter_vars=None,
               cascade=True):
        '''
        delete an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param filter: filter the object list
        :type filter: string
        :param filter_vars: variables used in the filter expression
        :type filter_vars: dict
        :param cascade: deleted dependent objects
        :type joins: bool

        example 1:
        delete('Host', 'localhost')

        example 2:
        delete('Service', filter='match("vhost*", service.name)')
        '''

        object_type_url_path = self._convert_object_type(object_type)

        payload = {}
        if filter:
            payload['filter'] = filter
        if filter_vars:
            payload['filter_vars'] = filter_vars
        if cascade:
            payload['cascade'] = 1

        url = '{}/{}'.format(self.base_url_path, object_type_url_path)
        if name:
            url += '/{}'.format(name)

        return self._request('DELETE', url, payload)
