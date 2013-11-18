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

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

from galloper.openstack.common.db.sqlalchemy import session as db_session
from galloper.db.api import Connection as AConnection
from galloper.db import Node
from galloper.common.exceptions import NodeNotFound
from galloper.common.exceptions import MultipleNodesFound


def get_backend():
    """This method is called from openstack.common.db.api.DBAPI
    to get backend. openstack.common.db.api.DBAPI.__getattr__ method
    tries to get attribute from backend. So we can call Connection instance
    method as if they were openstack.common.db.api.DBAPI instance methods."""
    return Connection()


def model_query(model, session=None):
    session = session or db_session.get_session()
    query = session.query(model)
    return query


class Connection(AConnection):
    """SqlAlchemy connection."""

    def get_db_nodes(self):
        query = model_query(Node)
        return iter(query)

    def get_nodes(self):
        for db_node in self.get_db_nodes():
            yield Node.from_db(db_node)

    def get_db_node(self, uuid):
        query = model_query(Node)
        query.filter_by(uuid=uuid)
        try:
            obj = query.one()
        except NoResultFound:
            raise NodeNotFound(uuid=uuid)
        except MultipleResultsFound:
            raise MultipleNodesFound(uuid=uuid)
        return obj

    def get_node(self, uuid):
        return Node.from_db(self.get_db_node(uuid))

    def create_node(self, data):
        for name, generator in Node.default_generators:
            if not data.get(name):
                data[name] = generator()
        node = Node()
        node.update(values)
        node.save()
        return node


    def destroy_node(self, uuid):
        pass

    def update_db_node(self, uuid, data):
        session = db_session.get_session()
        with session.begin():
            query = model_query(Node, session=session)
            query.filter_by(uuid=uuid)

            count = query.update(data, synchronize_session='fetch')
            if count < 1:
                raise NodeNotFound(uuid=uuid)
            elif count > 1:
                raise MultipleNodesFound(uuid=uuid)
            obj = query.one()
        return obj

    def update_node(self, uuid, data):
        self.update_db_node(uuid, data)
