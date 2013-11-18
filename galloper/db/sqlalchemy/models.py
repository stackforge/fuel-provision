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

import json

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import schema, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR

from galloper.openstack.common.db.sqlalchemy import models


class JSON(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class GalloperBase(models.ModelBase):
    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


Base = declarative_base(cls=GalloperBase)


class Node(Base):
    __tablename__ = 'nodes'
    __table_args__ = (schema.UniqueConstraint('uuid', name='node_uuid_ux'))
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), index=True)
    meta = Column(JSON)


class Image(Base):
    __tablename__ = 'images'
    __table_args__ = (schema.UniqueConstraint('uuid', name='node_uuid_ux'))
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), index=True)
    meta = Column(JSON)


