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

import functools
import json
import sys
import yaml


def branch(func):
    if hasattr(func, 'is_subtree') and func.is_subtree:
        raise Exception("Incompatible decorator: only one of "
                        "'branch' and 'subtree' should be used")
    func.is_branch = True
    return func


def subtree(branches):
    if not isinstance(branches, (list, tuple)):
        branches = [branches]
    branches = list(branches)

    def wrapper(func):
        if hasattr(func, 'is_branch') and func.is_branch:
            raise Exception("Incompatible decorator: only one of "
                            "'branch' and 'subtree' should be used")
        func.is_subtree = True
        func.branches = branches
        return func
    return wrapper


def arg(*args, **kwargs):
    def wrapper(func):
        if not hasattr(func, 'args'):
            func.args = []
        if (args, kwargs) not in func.args:
            func.args.insert(0, (args, kwargs))
        return func
    return wrapper


"""TODO(kozhukalov): Create default arguments decorator
"""


def printer(data, formatted="", indent=0):
    """Custom print method. Almost the same as yaml.safe_dump()."""

    """TODO(kozhukalov): it is almost the same as yaml, so it might be better
    to remove this print method
    """
    newformatted = formatted
    if isinstance(data, (int, float, str, unicode)):
        newformatted += " " * indent + "- " + str(data) + "\n"
    elif isinstance(data, (list,)):
        for newdata in data:
            newformatted += printer(newdata, formatted, indent + 4)
    elif isinstance(data, (dict,)):
        for key, value in data.iteritems():
            newformatted += " " * indent + str(key) + ":\n"
            newformatted += printer(value, formatted, indent + 4)
    return newformatted


def print_formatted(data, method='yaml', custom=None):
    try:
        formatted = {
            'custom': (custom if custom else printer),
            'json': functools.partial(json.dumps, indent=4),
            'yaml': functools.partial(yaml.safe_dump, default_flow_style=False)
        }[method](data)
        sys.stdout.write(formatted)
    except:
        sys.stdout.write("Error occured while trying to print the result")
        sys.exit(1)


@branch
def info(http_client, *args, **kwargs):
    """Print information about galloper provisioning system"""
    print_formatted(http_client.get('')[1])


@subtree('node')
def node(*args, **kwargs):
    """Node subcommand."""
    pass


@subtree('image')
def image(*args, **kwargs):
    """Image subcommand."""
    pass
