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


class InfoHandler(CommandHandler):

    def __init__(self, config):
        super(InfoHandler, self).__init__(config)
        self.jira_client = JiraClient(config.get_endpoint('jira'),
                                      config.get_auth())
        self.bamboo_client = BambooClient(config.get_endpoint('bamboo'),
                                          config.get_auth())
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
