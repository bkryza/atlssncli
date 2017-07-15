import requests
import exceptions
import click
import logging as LOG
import json
from humanfriendly.tables import format_pretty_table

from config import Config
from commandhandler import CommandHandler
from querybuilder import QueryBuilder
from rest.jiraclient import JiraClient

class ProjectHandler(CommandHandler):

    def __init__(self, config):
        super(ProjectHandler, self).__init__(config) 
        self.client = JiraClient(config.get_endpoint('jira'), 
                                 config.get_auth())
        self.qb = QueryBuilder(config)
        pass

    def get_project_components(self, project):
        """Show project components.
        """
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
        LOG.debug('Getting project issue types: %s', project)
        
        res = self.client.get_project(project)

        if not 'issueTypes' in res:
            res['issueTypes'] = []

        column_names = ['ID', 'Name']
        issue_types = []
        for issue_type in res['issueTypes']:
            issue_types.append([issue_type['id'], issue_type['name']])

        click.echo(format_pretty_table(issue_types, column_names))

    def get_project_details(self, project):
        """Show basic information about the project.
        """
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
        #if 'components' in res:
        #    project_details.append(['components', 
        #        ",".join(list(map(lambda x: x['name'], res['components'])))])
        #if 'issueTypes' in res:
        #    project_details.append(['roles', list(map(lambda x: x['name'], res[])))

        click.echo(format_pretty_table(project_details, column_names))

    def list_projects(self):
        """List all projects.
        """
        LOG.debug("Listing projects...")

        res = self.client.get_all_projects()

        column_names = ['Key', 'ID', 'Name']
        projects = []
        for project in res:
            projects.append([project['key'], project['id'], project['name']])
        
        #  LOG.debug(projects)
        click.echo(format_pretty_table(projects, column_names))

    def select_project(self, project):


        pass

    def create_project(self, project):

        pass

    def delete_project(self, project):
        
        pass

