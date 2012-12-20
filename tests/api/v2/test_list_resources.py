# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Test listing resources.
"""

import datetime
import logging

from ceilometer.collector import meter
from ceilometer import counter
from ceilometer.openstack.common import cfg

from .base import FunctionalTest

LOG = logging.getLogger(__name__)


class TestListResources(FunctionalTest):

    SOURCE_DATA = {'test_list_resources': {}}

    def test_empty(self):
        data = self.get_json('/resources')
        self.assertEquals([], data)

    def test_instances(self):
        counter1 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id',
            timestamp=datetime.datetime(2012, 7, 2, 10, 40),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter',
                               }
            )
        msg = meter.meter_message_from_counter(counter1,
                                               cfg.CONF.metering_secret,
                                               'test',
                                               )
        self.conn.record_metering_data(msg)

        counter2 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id-alternate',
            timestamp=datetime.datetime(2012, 7, 2, 10, 41),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter2',
                               }
            )
        msg2 = meter.meter_message_from_counter(counter2,
                                                cfg.CONF.metering_secret,
                                                'test',
                                                )
        self.conn.record_metering_data(msg2)

        data = self.get_json('/resources')
        self.assertEquals(2, len(data))

    def test_with_source(self):
        counter1 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id',
            timestamp=datetime.datetime(2012, 7, 2, 10, 40),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter',
                               }
            )
        msg = meter.meter_message_from_counter(counter1,
                                               cfg.CONF.metering_secret,
                                               'test_list_resources',
                                               )
        self.conn.record_metering_data(msg)

        counter2 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id2',
            'project-id',
            'resource-id-alternate',
            timestamp=datetime.datetime(2012, 7, 2, 10, 41),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter2',
                               }
            )
        msg2 = meter.meter_message_from_counter(counter2,
                                                cfg.CONF.metering_secret,
                                                'not-test',
                                                )
        self.conn.record_metering_data(msg2)

        data = self.get_json('/sources/test_list_resources/resources')
        ids = [r['resource_id'] for r in data]
        self.assertEquals(['resource-id'], ids)

    def test_with_user(self):
        counter1 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id',
            timestamp=datetime.datetime(2012, 7, 2, 10, 40),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter',
                               }
            )
        msg = meter.meter_message_from_counter(counter1,
                                               cfg.CONF.metering_secret,
                                               'test_list_resources',
                                               )
        self.conn.record_metering_data(msg)

        counter2 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id2',
            'project-id',
            'resource-id-alternate',
            timestamp=datetime.datetime(2012, 7, 2, 10, 41),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter2',
                               }
            )
        msg2 = meter.meter_message_from_counter(counter2,
                                                cfg.CONF.metering_secret,
                                                'not-test',
                                                )
        self.conn.record_metering_data(msg2)

        data = self.get_json('/users/user-id/resources')
        ids = [r['resource_id'] for r in data]
        self.assertEquals(['resource-id'], ids)

    def test_with_project(self):
        counter1 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id',
            timestamp=datetime.datetime(2012, 7, 2, 10, 40),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter',
                               }
            )
        msg = meter.meter_message_from_counter(counter1,
                                               cfg.CONF.metering_secret,
                                               'test_list_resources',
                                               )
        self.conn.record_metering_data(msg)

        counter2 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id2',
            'project-id2',
            'resource-id-alternate',
            timestamp=datetime.datetime(2012, 7, 2, 10, 41),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter2',
                               }
            )
        msg2 = meter.meter_message_from_counter(counter2,
                                                cfg.CONF.metering_secret,
                                                'not-test',
                                                )
        self.conn.record_metering_data(msg2)

        data = self.get_json('/projects/project-id/resources')
        ids = [r['resource_id'] for r in data]
        self.assertEquals(['resource-id'], ids)

    def test_metadata(self):
        counter1 = counter.Counter(
            'instance',
            'cumulative',
            1,
            'user-id',
            'project-id',
            'resource-id',
            timestamp=datetime.datetime(2012, 7, 2, 10, 40),
            resource_metadata={'display_name': 'test-server',
                               'tag': 'self.counter',
                               'ignored_dict': {'key': 'value'},
                               'ignored_list': ['not-returned'],
                               }
            )
        msg = meter.meter_message_from_counter(counter1,
                                               cfg.CONF.metering_secret,
                                               'test',
                                               )
        self.conn.record_metering_data(msg)

        data = self.get_json('/resources')
        metadata = data[0]['metadata']
        self.assertEqual(
            list(sorted(metadata.iteritems())),
            [('display_name', 'test-server'),
             ('tag', 'self.counter'),
             ])