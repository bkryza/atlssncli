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

import util

from config import Config
from commandhandler import CommandHandler
from rest.agileclient import AgileClient
from requests.auth import HTTPBasicAuth
from dateutil.parser import parse
import cached


class BoardHandler(CommandHandler):

    def __init__(self, config):
        super(BoardHandler, self).__init__(config)
        self.client = AgileClient(config.get_endpoint('agile'))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))
        pass

    def get_board_list(self, board_type):
        """Show board list."""
        LOG.debug('Getting board list')

        res = self.client.get_boards(board_type)

        self._render_board_list(res)

    def get_board_status(self, board_id):
        """Show board status."""
        LOG.debug('Getting board list')

        if not board_id:
            board_id = self.config.get_board()

        res = self.client.get_board(board_id)

        self._render_board_list([res])

    def get_board_backlog(self, board_id, assignee, jql):
        """Show board status."""
        LOG.debug('Getting board backlog: %s', board_id)

        if assignee and jql:
            raise 'Specifying assignee and JQL together doesn\'t make sense'

        if not board_id:
            board_id = self.config.get_board()

        if assignee:
            jql = "assignee={}".format(assignee, )

        res = self.client.get_board_backlog(board_id, jql)

        self._render_board_backlog(res)

    def get_board_versions(self, board_id, released):
        """List board release versions."""
        LOG.debug('Getting board release versions: %s', board_id)

        if not board_id:
            board_id = self.config.get_board()

        is_last, versions = \
            self.client.get_board_versions(board_id, released)

        self._render_board_versions(versions)

    def _render_board_list(self, boards):
        """Render board list."""

        column_names = ['ID', 'Name', 'Type']
        values = []
        for board in boards:
            values.append(
                [str(board['id']), board['name'], board['type']])

        click.echo(format_pretty_table(values, column_names))

    def _render_board_backlog(self, issues):
        """Render backlog issues."""

        LOG.debug("Rendering board backlog %s", str(issues))

        column_names = ['ID', 'Name', 'Reporter', 'Assignee']
        values = []
        for i in issues:
            values.append(
                [str(i['key']),
                 util.get(i, '-', 'fields', 'summary'),
                 util.get(i, '-', 'fields', 'reporter', 'name'),
                 util.get(i, '-', 'fields', 'assignee', 'name')])

        click.echo(format_pretty_table(values, column_names))

    def _render_board_versions(self, versions):
        """Render board release versions."""

        LOG.debug("Rendering board versions %s", str(versions))

        column_names = ['ID', 'Project ID', 'Name', 'Description']
        values = []
        for i in versions:
            values.append(
                [str(i['id']),
                 str(i['projectId']),
                 str(i['name']),
                 str(i.get('description', '-'))])

        click.echo(format_pretty_table(values, column_names))
