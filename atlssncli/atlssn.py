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

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

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


@click.group(context_settings={'help_option_names':['-h','--help']})
@click.option('-v', '--verbose', count=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """Command line interface to Atlassian services."""
    # Initialize logging based on 'verbose' flag
    if verbose == 0:
        LOG.basicConfig(stream=sys.stderr, level=LOG.ERROR)
    else:
        LOG.basicConfig(stream=sys.stderr, level=LOG.DEBUG)

    try:
        config = Config()
        config.validate()
        ctx.obj = {}
        ctx.obj['CONFIG'] = config
    except Exception as e:
        LOG.error("Configuration error")
        raise click.ClickException(e.message)

@cli.command()
@click.pass_context
def help(ctx):
    """Print help"""
    click.echo(ctx.parent.get_help())

@cli.command()
@click.pass_context
def version(ctx):
    """Print version"""
    click.echo("0.0.1")


#
# PROJECT GROUP
#
@cli.group()
@click.pass_context
def project(ctx):
    """Manage projects"""
    ctx.obj = Project(ctx.obj['CONFIG'])

@project.command()
@pass_project
def create(project):
    """Create new project."""
    click.echo('CREATE...')

@project.command()
@pass_project
def list(project):
    """List all projects.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.list_projects()
    except Exception as e:
        raise click.ClickException(e.message)

@project.command()
@click.argument('project_id', 'Project id or key.')
@pass_project
def info(project, project_id):
    """Get project details.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_details(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

@project.command('list-components')
@click.argument('project_id', 'Project id or key.')
@pass_project
def list_components(project, project_id):
    """List project components.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_components(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

@project.command('list-issue-types')
@click.argument('project_id', 'Project id or key.')
@pass_project
def list_components(project, project_id):
    """List project issue types.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_issue_types(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

@project.command()
@click.argument('name')
@pass_project
def select(project, name):
    """Select active project

       All consecutive commands will be performed in the scope of that project.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.select_project(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

#
# ISSUE GROUP
#
@cli.group()
@click.pass_context
def issue(ctx):
    """Manage issues
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

