import click

from commandgroup import *
from infohandler import InfoHandler

pass_info = click.make_pass_decorator(Info)

#
# INFO GROUP
#
@click.group()
@click.pass_context
def info(ctx):
    """Show information about configured Atlassian services"""
    ctx.obj = Info(ctx.obj['CONFIG'])

@info.command()
@click.pass_context
def help(ctx):
    """Print info command help"""
    click.echo(ctx.parent.get_help())

@info.command()
@pass_info
def jira(info):
    """Show information about JIRA service"""
    try:
        handler = InfoHandler(info.get_config())
        handler.show_jira_info()
    except Exception as e:
        raise click.ClickException(e.message)

@info.command()
@pass_info
def bamboo(info):
    """Show information about Bamboo service"""
    try:
        handler = InfoHandler(info.get_config())
        handler.show_bamboo_info()
    except Exception as e:
        raise click.ClickException(e.message)
