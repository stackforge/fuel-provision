# Copyright 2013: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from galloper.db import api as db_api
from galloper.openstack.common import uuidutils


class Node(object):
    """This method returns openstack.common.db.api.DBAPI instance.
    When we call methods we actually call instance methods from
    backend which is instance of AConnection subclass.
    """
    dbapi = db_api.get_instance()
    fields = ('id', 'uuid', 'meta')
    default_generators = {
        'uuid': uuidutils.generate_uuid,
        'meta': lambda: {}
    }

    @classmethod
    def from_db(cls, db_node):
        """Converts a database entity to a formal object."""
        node = cls()
        for field in cls.fields:
            node[field] = db_node[field]
        return node

    @classmethod
    def get_by_uuid(cls, uuid):
        """Find a node based on uuid and return a Node object.

        :param uuid: the uuid of a node.
        :returns: a :class:`Node` object.
        """
        db_node = cls.dbapi.get_node(uuid)
        return Node.from_db(db_node)

    def to_data(self):
        data = {}
        for field in self.fields:
            data[field] = getattr(self, field)
        return data

    def save(self):
        self.dbapi.update_node(self.uuid, self.to_data())

    def refresh(self):
        actual = self.__class__.get_by_uuid(self.uuid)
        for field in self.fields:
            if (hasattr(self, field) and
                        getattr(self, field) != getattr(actual, field)):
                setattr(self, field, getattr(actual, field))
