# -*- coding: utf-8 -*-
#
# Copyright 2019 Bartosz Kryza <bkryza@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import exceptions
import click
import logging as LOG
import json
import gitcontext
from datetime import datetime, timedelta
from humanfriendly.tables import format_pretty_table

from config import Config
from commandhandler import CommandHandler
from rest.bambooclient import BambooClient
from requests.auth import HTTPBasicAuth
from dateutil.parser import parse
import cached


class AgentHandler(CommandHandler):

    def __init__(self, config):
        super(AgentHandler, self).__init__(config)
        self.client = BambooClient(config.get_endpoint('bamboo'))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))
        pass

    def get_agent_list(self):
        """Show agent list."""
        LOG.debug('Getting agent list')

        res = self.client.get_agents()

        self._render_agent_list(res)

    def _render_agent_list(self, agents):
        """Render agent list."""

        column_names = ['ID', 'Name', 'Type', 'Active', 'Enabled', 'Busy']
        values = []
        for agent in agents:
            values.append(
                [str(agent['id']), agent['name'], agent['type'],
                 str(agent['active']), str(agent['enabled']),
                 str(agent['busy'])])

        click.echo(format_pretty_table(values, column_names))
