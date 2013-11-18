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


from galloper.cli.v1 import branch
from galloper.cli.v1 import arg


@branch
@arg('-a', '--all',
     action='store_true',
     dest='node_list_all',
     default=False,
     help="List all nodes.")
def list(http_client, *args, **kwargs):
    """List available nodes."""
    pass


@branch
@arg('-n', '--name',
     action='store',
     dest='node_create_name',
     help="Name of node to create.")
def create(http_client, *args, **kwargs):
    """Create new node."""
    pass


@branch
@arg('-n', '--name',
     action='store',
     dest='node_edit_name',
     help="Name of node to edit.")
def edit(http_client, *args, **kwargs):
    """Edit existing node."""
    pass

