import os
import sys
import posixpath
import requests
import exceptions
import click
import logging as LOG
import json
from humanfriendly.tables import format_pretty_table

from config import Config
from projecthandler import ProjectHandler
from issuehandler import IssueHandler


LOG.basicConfig(stream=sys.stderr, level=LOG.DEBUG)

class Project(object):
    def __init__(self, config):
        self.config = config
        pass
    def get_config(self):
        return self.config

class Issue(object):
    def __init__(self, config):
        self.config = config
        pass
    def get_config(self):
        return self.config

pass_project = click.make_pass_decorator(Project)
pass_issue = click.make_pass_decorator(Issue)


@click.group()
@click.pass_context
def cli(ctx):
    """Command line interface to Atlassian services."""
    #
    # Check if configuration directory is present
    # contains necessary files
    try:
        config = Config()
        config.validate()
        ctx.obj = {}
        ctx.obj['CONFIG'] = config
    except Exception as e:
        LOG.error("Configuration error")
        raise click.ClickException(e.message)


@cli.group()
@click.pass_context
def project(ctx):
    """Manage projects."""
    ctx.obj = Project(ctx.obj['CONFIG'])

@project.command()
@pass_project
def create(project):
    """Create new project."""
    click.echo('CREATE...')
    pass

@project.command()
@pass_project
def list(project):
    """List all your projects.
    """
    handler = ProjectHandler(project.get_config())
    handler.list_projects()

@project.command()
@click.argument('name')
@pass_project
def select(project, name):
    """Select active project. 

       All consecutive commands will be performed in the scope of that project.
    """
    LOG.debug('Switching to project %s', name)


    pass


@cli.group()
@click.pass_context
def issue(ctx):
    """
    """
    ctx.obj = Issue()


@issue.command()
@pass_issue
def create(issue):
    click.echo('CREATE...')
    pass


@issue.command()
@pass_issue
def resolve(issue):
    click.echo('CREATE...')
    pass

