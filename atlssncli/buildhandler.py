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

class BuildHandler(CommandHandler):

    def __init__(self, config):
        super(BuildHandler, self).__init__(config)
        self.client = BambooClient(config.get_endpoint('bamboo'),
                                 config.get_auth())
        self.qb = QueryBuilder(config)
        pass

    def get_project_plans(self, project):
        """Show project build plans.
        """
        LOG.debug('Getting project build plans: %s', project)
        
        res = self.client.get_project(project)

        if not 'components' in res:
            res['components'] = []

        column_names = ['ID', 'Name']
        components = []
        for component in res['components']:
            components.append([component['id'], component['name']])

        click.echo(format_pretty_table(components, column_names))

    #  def get_project_issue_types(self, project):
    #      """Show project issue types.
    #      """
    #      LOG.debug('Getting project issue types: %s', project)
    #
    #      res = self.client.get_project(project)
    #
    #      if not 'issueTypes' in res:
    #          res['issueTypes'] = []
    #
    #      column_names = ['ID', 'Name']
    #      issue_types = []
    #      for issue_type in res['issueTypes']:
    #          issue_types.append([issue_type['id'], issue_type['name']])
    #
    #      click.echo(format_pretty_table(issue_types, column_names))

