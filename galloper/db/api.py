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

import abc

from galloper.openstack.common.db import api as db_api

_BACKEND_MAPPING = {'sqlalchemy': 'galloper.db.sqlalchemy.api'}
IMPL = db_api.DBAPI(backend_mapping=_BACKEND_MAPPING)


def get_instance():
    """Returns openstack.common.db.api.DBAPI instance"""
    return IMPL


class Connection(object):
    """Base class for storage system connections."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """Constructor."""

    @abc.abstractmethod
    def get_nodes(self):
        """Return a list of dicts of all nodes.
        """

    @abc.abstractmethod
    def get_node(self, uuid):
        """Return a dict representing node.

        :param uuid: Node uuid
        """

    @abc.abstractmethod
    def create_node(self, data):
        """Create a new node.

        :param data: A dict containing node data.
        :returns: A node.
        """

    @abc.abstractmethod
    def destroy_node(self, uuid):
        """Destroy a node.

        :param uuid: The uuid of a node.
        """

    @abc.abstractmethod
    def update_node(self, uuid, data):
        """Update properties of a node.

        :param node: The uuid of a node.
        :param data: Dict of containing node data to update.
        :returns: A node.
        """
