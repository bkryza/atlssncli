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
from humanfriendly.tables import format_pretty_table
from requests.auth import HTTPBasicAuth

from .config import Config
from .commandhandler import CommandHandler
from .querybuilder import QueryBuilder
from .rest.jiraclient import JiraClient


class ProjectHandler(CommandHandler):

    def __init__(self, config):
        super(ProjectHandler, self).__init__(config)
        self.client = JiraClient(config.get_endpoint('jira'))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))
        pass

    def get_project_components(self, project):
        """Show project components.
        """
        if not project:
            project = self.config.get_project()

        if not project:
            LOG.error('No project specified')
            raise 'No project specified'

        LOG.debug('Getting project components: %s', project)

        res = self.client.get_project(project)

        if not 'components' in res:
            res['components'] = []

        column_names = ['ID', 'Name']
        components = []
        for component in res['components']:
            components.append([component['id'], component['name']])

        click.echo(format_pretty_table(components, column_names))

    def get_project_issue_types(self, project):
        """Show project issue types.
        """
        if not project:
            project = self.config.get_project()

        if not project:
            LOG.error('No project specified')
            raise 'No project specified'

        LOG.debug('Getting project issue types: %s', project)

        res = self.client.get_project(project)

        if 'issueTypes' not in res:
            res['issueTypes'] = []

        column_names = ['ID', 'Name']
        issue_types = []
        for issue_type in res['issueTypes']:
            issue_types.append([issue_type['id'], issue_type['name']])

        click.echo(format_pretty_table(issue_types, column_names))

    def get_project_details(self, project):
        """Show basic information about the project.
        """
        if not project:
            project = self.config.get_project()

        if not project:
            LOG.error('No project specified')
            raise 'No project specified'

        LOG.debug('Getting project information: %s', project)

        res = self.client.get_project(project)

        column_names = ['Property', 'Value']
        project_details = []
        if 'key' in res:
            project_details.append(['key', res['key']])
        if 'id' in res:
            project_details.append(['id', res['id']])
        if 'name' in res:
            project_details.append(['name', res['name']])
        if 'lead' in res:
            if 'displayName' in res['lead']:
                project_details.append(['lead', res['lead']['displayName']])
            else:
                project_details.append(['lead', res['lead']['name']])
        if 'url' in res:
            project_details.append(['url', res['url']])
        click.echo(format_pretty_table(project_details, column_names))

    def list_projects(self):
        """List all projects"""
        LOG.debug("Listing projects...")

        res = self.client.get_all_projects()

        column_names = ['Key', 'ID', 'Name']
        projects = []
        for project in res:
            projects.append([project['key'], project['id'], project['name']])

        click.echo(format_pretty_table(projects, column_names))

    def select_project(self, project):
        """Select active project"""

        active_project = None
        if not project:
            active_project = self.config.get_project()
        else:
            self.config.set_project(project)
            active_project = project

        if not active_project:
            click.echo("You have not selected active project")
        else:
            click.echo("Active project: %s" % (active_project))

    def create_project(self, project):
        pass

    def delete_project(self, project):
        pass
