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
from humanfriendly.tables import format_pretty_table, format_smart_table

from config import Config
from commandhandler import CommandHandler
from querybuilder import QueryBuilder
from rest.jiraclient import JiraClient
from rest.bambooclient import BambooClient
from requests.auth import HTTPBasicAuth


class InfoHandler(CommandHandler):

    def __init__(self, config):
        super(InfoHandler, self).__init__(config)
        self.jira_client = JiraClient(config.get_endpoint('jira'))
        self.jira_client._set_auth(HTTPBasicAuth(*config.get_auth()))
        self.bamboo_client = BambooClient(config.get_endpoint('bamboo'))
        self.bamboo_client._set_auth(HTTPBasicAuth(*config.get_auth()))
        self.qb = QueryBuilder(config)
        pass

    def show_jira_info(self):
        """Show JIRA service information.
        """
        LOG.debug('Showing JIRA service information: %s')

        res = self.jira_client.get_info()

        data = []
        data.append(["URL", res['baseUrl']])
        data.append(["Version", res['version']])
        data.append(["Build number", res['buildNumber']])
        data.append(["Server title", res['serverTitle']])

        click.echo(format_smart_table(data, []))

    def show_bamboo_info(self):
        """Show Bamboo service information.
        """
        LOG.debug('Showing Bamboo service information: %s')

        res = self.bamboo_client.get_info()

        data = []
        data.append(["Version", res['version']])
        data.append(["Build number", res['buildNumber']])
        data.append(["State", res['state']])

        click.echo(format_smart_table(data, []))
