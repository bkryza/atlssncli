import requests
import exceptions
import click
import logging as LOG
import json
from humanfriendly.tables import format_pretty_table

from config import Config
from commandhandler import CommandHandler
from querybuilder import QueryBuilder
from rest.bambooclient import BambooClient


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

        if 'components' not in res:
            res['components'] = []

        column_names = ['ID', 'Name']
        components = []
        for component in res['components']:
            components.append([component['id'], component['name']])

        click.echo(format_pretty_table(components, column_names))

    def get_build_queue(self):
        """Show build queue.
        """
        LOG.debug('Getting Bamboo build queue')

        res = self.client.get_queue()

        if 'queuedBuilds' not in res:
            LOG.error('queuedBuilds not expanded in response')

        if 'queuedBuild' not in res['queuedBuilds']:
            LOG.error('queuedBuild not expanded in response queuedBuilds')

        column_names = ['Key', 'Build #', 'Reason']
        builds = []
        for build in res['queuedBuilds']['queuedBuild']:
            builds.append([build['planKey'],
                           build['buildNumber'],
                           build['triggerReason']])

        click.echo(format_pretty_table(builds, column_names))

    def build_plan(self, plan_id):
        """Show build queue.
        """
        LOG.debug('Queuing build plan: %s' % (plan_id))

        res = self.client.build_plan(plan_id)

        build_link = res['link']['href']
        build_plan_key = res['planKey']
        build_number = res['buildNumber']

        click.echo("Scheduled build %d for %s at: %s" %
                   (build_number, build_plan_key, build_link))
