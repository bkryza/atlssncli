import click
from commandgroup import *

pass_docs = click.make_pass_decorator(Docs)

#
# DOCUMENT GROUP
#


@click.group()
@click.pass_context
def docs(ctx):
    """Document management"""
    ctx.obj = Docs(ctx.obj['CONFIG'])


@docs.command()
@click.pass_context
def help(ctx):
    """Print document command help"""
    click.echo(ctx.parent.get_help())


@docs.command('list-spaces')
@pass_docs
def list_spaces(docs, page, format):
    """List existing spaces"""
    click.echo(ctx.parent.get_help())


@docs.command('create-space')
@click.argument('space')
@pass_docs
def create_space(docs, space):
    """Create new space"""
    click.echo(ctx.parent.get_help())


@docs.command('delete-space')
@click.argument('space')
@pass_docs
def delete_space(docs, space):
    """Delete existing space"""
    click.echo(ctx.parent.get_help())


@docs.command('show-page')
@click.argument('page')
@click.option('-f', '--format', help='Print output in specific format')
@pass_docs
def show_page(docs, page, format):
    """Show specific page"""
    click.echo(ctx.parent.get_help())
