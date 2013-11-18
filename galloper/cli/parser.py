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


import argparse
import importlib

from galloper.cli.client import HTTPClient


class GalloperCli(object):
    SHELL_ROOT = 'galloper.cli'

    def shell(self, parser, version='v1', shell_root=None,
              shell_module_path=None):

        def traverse(module_path, par):
            module = importlib.import_module(module_path)
            sub_parsers = par.add_subparsers(dest='subcommand',
                                             metavar='<subcommand>')

            for attr in dir(module):
                func = getattr(module, attr)

                if (not hasattr(func, 'is_branch') and
                        not hasattr(func, 'is_subtree')):
                    continue

                description = func.__doc__ or ''
                sub_parser = sub_parsers.add_parser(
                    attr.replace('_', '-'),
                    help=description.strip(),
                    description=description,
                    add_help=True,
                )
                if hasattr(func, 'is_branch') and func.is_branch:
                    for (args, kwargs) in getattr(func, 'args', []):
                        sub_parser.add_argument(*args, **kwargs)
                    sub_parser.set_defaults(func=func)
                elif hasattr(func, 'is_subtree') and func.is_subtree:
                    for branch in func.branches:
                        sub_parser = traverse(module_path + '.' + branch,
                                              sub_parser)
            return par

        if not shell_root:
            shell_root = self.SHELL_ROOT
        if not shell_module_path:
            shell_module_path = shell_root + '.' + version
        return traverse(shell_module_path, parser)

    def main(self, argv):
        parser = argparse.ArgumentParser(
            prog='galloper',
            description='Command line interface to the '
                        'galloper provisioning system',
            add_help=True,
        )
        parser.add_argument(
            '--cli-version',
            action='store',
            dest='cli_version',
            default='v1',
            help='Command line interface version.'
        )

        parser = self.shell(parser)
        (options, args) = parser.parse_known_args(argv)

        if options.func:
            http_client = HTTPClient()
            options.func(http_client, *args)
