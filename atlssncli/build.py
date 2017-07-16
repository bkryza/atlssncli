import click
from commandgroup import *


pass_build = click.make_pass_decorator(Build)


#
# BUILD GROUP
#
@click.group()
@click.pass_context
def build(ctx):
    """Build management"""
    ctx.obj = Build(ctx.obj['CONFIG'])

@build.command()
@click.pass_context
def help(ctx):
    """Print build command help"""
    click.echo(ctx.parent.get_help())


