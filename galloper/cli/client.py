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
import requests
import urlparse
from oslo.config import cfg

from galloper.common import exceptions
from galloper.openstack.common import log as logging


cli_client_opts = [
    cfg.StrOpt('galloper_cli_user_agent',
               default='galloper-cli',
               help='Galloper CLI user agent.'),
    cfg.StrOpt('galloper_api_host',
               default='0.0.0.0',
               help='Galloper API host.'),
    cfg.IntOpt('galloper_api_port',
               default=9999,
               help='Galloper API port number.'),
]


CONF = cfg.CONF
CONF.register_opts(cli_client_opts)
LOG = logging.getLogger("galloper-cli")


class HTTPClient(object):
    USER_AGENT = CONF.galloper_cli_user_agent
    BASE_URL = 'http://{0}:{1}'.format(CONF.galloper_api_host,
                                       CONF.galloper_api_port)

    def __init__(self):
        self.http = requests.Session()

    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)

    def request(self, url, method, **kwargs):
        if urlparse.urlparse(url).scheme != 'http':
            actual_url = urlparse.urljoin(self.BASE_URL, url)
        else:
            actual_url = url

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.USER_AGENT
        kwargs['headers']['Accept'] = 'application/json'
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs['body'])
            del kwargs['body']

        LOG.debug("Sending request to API: method={0} url={1} "
                  "kwargs={2}".format(method, actual_url, kwargs))
        resp = self.http.request(
            method,
            actual_url,
            **kwargs)

        """TODO(kozhukalov): accurate dealing with http
        """
        if resp.text:
            if resp.status_code == 400:
                if ('Connection refused' in resp.text or
                        'actively refused' in resp.text):
                    raise exceptions.HttpException(resp.text)
            try:
                body = json.loads(resp.text)
            except ValueError:
                body = None
        else:
            body = None

        if resp.status_code >= 400:
            raise exceptions.HttpException(resp.status_code)

        LOG.debug("Response: code={0} body={1}".format(resp.status_code, body))
        return resp, body
