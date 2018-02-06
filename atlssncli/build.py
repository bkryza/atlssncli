import click
from commandgroup import *
from buildhandler import BuildHandler
import logging as LOG


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


@build.command()
@click.argument('plan_id')
@pass_build
def plan(build, plan_id):
    """Add plan to build queue"""
    LOG.debug("Adding plan to build queue %s", plan_id)
    try:
        handler = BuildHandler(build.get_config())
        handler.build_plan(plan_id)
    except Exception as e:
        raise click.ClickException(e.message)


@build.command()
@click.argument('plan_id')
@pass_build
def status(plan, plan_id):
    """Get plan status"""
    LOG.debug("Getting plan status %s", issue)


@build.command()
@pass_build
def queue(build):
    """Get current build queue"""
    try:
        handler = BuildHandler(build.get_config())
        handler.get_build_queue()
    except Exception as e:
        raise click.ClickException(e.message)


@build.command('enable-branch')
@click.argument('plan_id')
@pass_build
def enable_branch(plan, plan_id, branch_name):
    """Create and/or enable branch for build plan"""
    pass


@build.command('disable-branch')
@click.argument('plan_id')
@click.argument('branch_name')
@pass_build
def create_branch(build, plan_id, branch_name):
    """Disable branch for build plan"""
    pass
