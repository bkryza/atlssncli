import requests
import exceptions
import click
import logging as LOG
import json
from humanfriendly.tables import format_pretty_table

from config import Config
from commandhandler import CommandHandler
from querybuilder import QueryBuilder

class ProjectHandler(CommandHandler):

    def __init__(self, config):
        super(ProjectHandler, self).__init__(config) 
        self.qb = QueryBuilder(config)
        pass

    def list_projects(self):
        LOG.debug("Listing projects...")
        LOG.debug('REQUEST: '+self.qb.project_endpoint())
        r = requests.get(self.qb.project_endpoint(), 
                         auth=self.config.get_auth())

        #  LOG.debug("RESPONSE: %s", r.json())
        column_names = ['ID', 'Name']
        projects = []
        for project in r.json():
            projects.append([project['id'], project['name']])
        
        #  LOG.debug(projects)
        click.echo(format_pretty_table(projects, column_names))

    def select_project(self, project):


        pass

    def create_project(self, project):

        pass

    def delete_project(self, project):
        
        pass

