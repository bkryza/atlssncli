import click

from commandgroup import *
from projecthandler import ProjectHandler

pass_project = click.make_pass_decorator(Project)

#
# PROJECT GROUP
#
@click.group()
@click.pass_context
def project(ctx):
    """Manage projects"""
    ctx.obj = Project(ctx.obj['CONFIG'])

@project.command()
@click.pass_context
def help(ctx):
    """Print project command help"""
    click.echo(ctx.parent.get_help())

@project.command()
@pass_project
def create(project):
    """Create new project"""

@project.command()
@pass_project
def list(project):
    """List all projects"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.list_projects()
    except Exception as e:
        raise click.ClickException(e.message)

@project.command()
@click.argument('project_id', 'Project id or key.')
@pass_project
def info(project, project_id):
    """Get project details"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_details(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

@project.command('list-components')
@click.argument('project_id', 'Project id or key.')
@pass_project
def list_components(project, project_id):
    """List project components"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_components(project_id)
    except Exception as e:
        raise click.ClickException(e.message)

@project.command('list-issue-types')
@click.argument('project_id', 'Project id or key.')
@pass_project
def list_components(project, project_id):
    """List project issue types"""
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


