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


from oslo.config import cfg
from wsgiref import simple_server

from galloper.openstack.common import log as logging
from galloper.api.app import WsgiApplication


api_opts = [
    cfg.StrOpt('galloper_api_host',
               default='0.0.0.0',
               help='Galloper API host.'),
    cfg.IntOpt('galloper_api_port',
               default=9999,
               help='Galloper API port number.'),
]


CONF = cfg.CONF
CONF.register_opts(api_opts)


def run():
    logging.setup("galloper-api")
    LOG = logging.getLogger("galloper-api")

    LOG.info("Starting galloper API host={0} port={1}".format(
        CONF.galloper_api_host, CONF.galloper_api_port
    ))
    wsgi = simple_server.make_server(CONF.galloper_api_host,
                                     CONF.galloper_api_port,
                                     WsgiApplication())

    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        LOG.info("Keyboard interruption caught. Stopping API.")

