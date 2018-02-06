import click
from commandgroup import *


pass_agile = click.make_pass_decorator(Agile)

#
# AGILE GROUP
#


@click.group()
@click.pass_context
def agile(ctx):
    """Sprint management"""
    ctx.obj = Agile(ctx.obj['CONFIG'])


@agile.command()
@click.pass_context
def help(ctx):
    """Print agile command help"""
    click.echo(ctx.parent.get_help())


@agile.command('create-sprint')
@click.argument('sprint')
@pass_agile
def create_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command('start-sprint')
@click.argument('sprint')
@pass_agile
def create_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command('close-sprint')
@pass_agile
def close_sprint(agile):
    """Close sprint"""
    click.echo(ctx.parent.get_help())


@agile.command('delete-sprint')
@click.argument('sprint')
@pass_agile
def delete_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command('sprint-status')
@pass_agile
def sprint_status(agile):
    """Get currently active sprint status"""
    click.echo(ctx.parent.get_help())
