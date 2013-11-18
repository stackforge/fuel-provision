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

import pecan


config = {
    'root': 'galloper.api.root.RootController',
    'modules': ['galloper.api'],
    'debug': True,
}


def setup_app(pecan_config=None):
    if not pecan_config:
        pecan_config = pecan.configuration.conf_from_dict(config)

    app = pecan.make_app(
        pecan_config.get('root'),
        debug=pecan_config.get('debug'),
    )
    return app


class WsgiApplication(object):

    def __init__(self):
        self.app = setup_app()

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
