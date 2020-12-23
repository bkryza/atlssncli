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
import click
import logging as LOG
import json
from humanfriendly.tables import format_pretty_table, format_robust_table
from requests.auth import HTTPBasicAuth

from .config import Config
from .commandhandler import CommandHandler
from .querybuilder import QueryBuilder
from .rest.jiraclient import JiraClient
from . import util


class IssueHandler(CommandHandler):

    def __init__(self, config):
        super(IssueHandler, self).__init__(config)
        self.client = JiraClient(config.get_endpoint('jira'))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))

    def get_issue_types(self, project_id=None):
        """Show issue types."""
        if not project_id:
            project_id = self.config.get_project()
            if not project_id:
                LOG.error('Cannot list issue types without project_id')
                raise 'Cannot list issue types without project_id'

        LOG.debug('Getting issue types for project: %s', project_id)

        res = self.client.get_issue_types(project_id)

        self._render_issue_types(res)

    def get_issue(self, issue_id):
        """Show issue."""
        LOG.debug('Getting issue: %s', issue_id)

        res = self.client.get_issue(issue_id)

        self._render_issues([res])

    def assign_issue(self, issue_id, assignee):
        """Assign issue."""
        LOG.debug('Assigning issue: %s', issue_id, assignee)

        self.client.assign_issue(issue_id, {'name': assignee})

    def _render_issue_types(self, issuetypes):
        """Render issue types."""

        column_names = ['ID', 'Name', 'Description']
        values = []
        for it in issuetypes:
            values.append(
                [str(it['id']), it['name'], it['description']])

        click.echo(format_pretty_table(values, column_names))

    def _render_issues(self, issues):
        """Render sprint issues."""

        column_names = ['ID', 'Key', 'Summary', 'Status', 'Assignee', 'Progress']
        values = []
        for issue in issues:
            values.append(
                [str(issue['id']), str(issue['key']),
                 str(util.get(issue, '-', 'fields', 'summary')),
                 str(util.get(issue, '-', 'fields', 'status', 'name')),
                 str(util.get(issue, 'Unassigned',
                              'fields', 'assignee', 'key')),
                 str(util.get(issue, '-', 'fields', 'progress', 'progress'))])

        if len(values) > 1:
            click.echo(format_pretty_table(values, column_names))
        else:
            click.echo(format_robust_table(values, column_names))
