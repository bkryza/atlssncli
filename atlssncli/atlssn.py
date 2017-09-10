import os
import sys
import posixpath
import requests
import exceptions
import click
import logging as LOG
import json

from config import Config
from issuehandler import IssueHandler
from commandgroup import *
from docs import docs
from agile import agile
from build import build
from git import git
from issue import issue
from project import project
from info import info
from . import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


pass_issue = click.make_pass_decorator(Issue)


@click.group(context_settings={'help_option_names':['-h','--help']})
@click.option('-v', '--verbose', count=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """
    Command line interface to Atlassian services.
    """
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
    click.echo(".".join(map(lambda x: str(x), __version__)))

@cli.command('update-cache')
@click.pass_context
def update_cache(ctx):
    """Update autocompletion cache"""

#
# Add command groups from separate modules
#
cli.add_command(project)
cli.add_command(issue)
cli.add_command(build)
cli.add_command(git)
cli.add_command(agile)
cli.add_command(docs)
cli.add_command(info)




