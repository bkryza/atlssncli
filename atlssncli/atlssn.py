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

class CommandGroup(object):
    def __init__(self, config):
        self.config = config
        pass
    def get_config(self):
        return self.config

class Project(CommandGroup):
    def __init__(self, config):
        super(Project, self).__init__(config)

class Issue(CommandGroup):
    def __init__(self, config):
        super(Issue, self).__init__(config)

class Git(CommandGroup):
    def __init__(self, config):
        super(Git, self).__init__(config)

class Build(CommandGroup):
    def __init__(self, config):
        super(Build, self).__init__(config)

class Agile(CommandGroup):
    def __init__(self, config):
        super(Agile, self).__init__(config)

class Docs(CommandGroup):
    def __init__(self, config):
        super(Docs, self).__init__(config)


pass_project = click.make_pass_decorator(Project)
pass_issue = click.make_pass_decorator(Issue)
pass_git = click.make_pass_decorator(Git)
pass_build = click.make_pass_decorator(Build)
pass_agile = click.make_pass_decorator(Agile)
pass_docs = click.make_pass_decorator(Docs)


@click.group(context_settings={'help_option_names':['-h','--help']})
@click.option('-v', '--verbose', count=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """Command line interface to Atlassian services."""
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
@click.pass_context
def help(ctx):
    """Print project command help"""
    click.echo(ctx.parent.get_help())

@project.command()
@pass_project
def create(project):
    """Create new project"""
    click.echo('CREATE...')

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

#
# ISSUE GROUP
#
@cli.group()
@click.pass_context
def issue(ctx):
    """Manage issues
    """
    ctx.obj = Issue(ctx.obj['CONFIG'])

@issue.command()
@click.pass_context
def help(ctx):
    """Print issue command help"""
    click.echo(ctx.parent.get_help())


@issue.command()
@click.argument('summary')
@click.option('-p', '--project', help='Project id')
@click.option('-t', '--issue-type', help='Issue type')
@click.option('-a', '--assignee', help='Assignee')
@click.option('-r', '--reporter', help='Reporter')
@click.option('-i', '--priority', help='Priority')
@click.option('-l', '--labels', help='Labels (comma separated)')
@click.option('-e', '--estimate', help='Initial estimate')
@click.option('-d', '--description', help='Description')
@click.option('-x', '--fix-versions', help='Fix versions')
@click.option('-u', '--duedate', help='Due date')
@click.option('-c', '--components', help='Components (comma separated)')
@pass_issue
def create(issue, summary, project, issue_type, assignee, reporter,
        priority, labels, estimate, description, fix_versions, duedate,
        components):
    """Create new issue"""
    LOG.debug("Creating issue %s (components: %s)", summary, components)
    pass

@issue.command()
@click.argument('issue')
@click.option('-p', '--project', help='Project id')
@click.option('-t', '--issue-type', help='Issue type')
@click.option('-a', '--assignee', help='Assignee')
@click.option('-r', '--reporter', help='Reporter')
@click.option('-i', '--priority', help='Priority')
@click.option('-l', '--labels', help='Labels (comma separated)')
@click.option('-e', '--estimate', help='Initial estimate')
@click.option('-d', '--description', help='Description')
@click.option('-x', '--fix-versions', help='Fix versions')
@click.option('-u', '--duedate', help='Due date')
@click.option('-c', '--components', help='Components (comma separated)')
@pass_issue
def modify(issue, summary, project, issue_type, assignee, reporter,
        priority, labels, estimate, description, fix_versions, duedate,
        components):
    """Modify existing issue"""
    LOG.debug("Modifying issue %s (components: %s)", summary, components)
    pass

@issue.command()
@click.argument('issue')
@pass_issue
def status(issue):
    """Get issue status"""
    pass

@issue.command()
@click.argument('issue')
@pass_issue
def delete(issue):
    """Delete issue"""
    pass

@issue.command()
@click.argument('issue')
@click.argument('assignee')
@pass_issue
def assign(issue):
    """Assign issue"""
    pass

@issue.command()
@click.argument('issue')
@click.argument('assignee')
@pass_issue
def assign(issue, assignee):
    """Assign issue"""
    pass

@issue.command('list-transitions')
@click.argument('issue')
@pass_issue
def list_transitions(issue):
    """List possible transitions"""
    pass

@issue.command('transition')
@click.argument('issue')
@click.argument('state')
@pass_issue
def transition(issue, state):
    """Transition the issue to another state"""
    pass

@issue.command('list-votes')
@click.argument('issue')
@pass_issue
def list_votes(issue):
    """List issue votes"""
    pass

@issue.command()
@click.argument('issue')
@pass_issue
def vote(issue):
    """Vote for an issue"""
    pass

@issue.command()
@click.argument('issue')
@pass_issue
def unvote(issue):
    """Unvote an issue"""
    pass

@issue.command('create-branch')
@click.argument('issue')
@click.argument('repository')
@click.argument('branch')
@pass_issue
def create_branch(issue, repository, branch):
    """Create an issue branch in repository from existing branch"""
    pass

@issue.command('list-branches')
@click.argument('issue')
@pass_issue
def list_branches(issue):
    """List branches created for this issue"""
    pass


#
# GIT GROUP
#
@cli.group()
@click.pass_context
def git(ctx):
    """Git repository management"""
    ctx.obj = Git(ctx.obj['CONFIG'])

@git.command()
@click.pass_context
def help(ctx):
    """Print Git command help"""
    click.echo(ctx.parent.get_help())

@git.command('list-ssh-keys')
@click.pass_context
def list_ssh_keys(ctx):
    """List Bitbucket SSH keys for this account"""
    pass

@git.command('add-ssh-key')
@click.pass_context
def add_ssh_key(ctx):
    """Add SSH key to Bitbucket for this account"""
    pass

@git.command('create-repository')
@click.argument('repository')
@pass_git
def create_repository(git):
    """Create repository"""
    pass

@git.command('create-pull-request')
@click.argument('repository')
@click.argument('source_branch')
@click.argument('target_branch')
@pass_git
def create_pull_request(git, source_branch, target_branch):
    """Create repository"""
    pass

@git.command('merge-pull-request')
@click.argument('repository')
@click.argument('pullrequest_id')
@pass_git
def merge_pull_request(git, pullrequest_id):
    """Merge pull request"""
    pass

@git.command('decline-pull-request')
@click.argument('repository')
@click.argument('pullrequest_id')
@pass_git
def decline_pull_request(git, pullrequest_id):
    """Decline pull request"""
    pass

@git.command('create-branch')
@click.argument('repository')
@click.argument('branch')
@pass_git
def create_branch(git, repository, branch):
    """Create branch"""
    pass

@git.command('delete-branch')
@click.argument('repository')
@click.argument('branch')
@pass_git
def delete_branch(git, repository, branch):
    """Delete branch"""
    pass

@git.command('delete-branch')
@click.argument('repository')
@pass_git
def list_branches(git, repository):
    """List branches"""
    pass


#
# AGILE GROUP
#
@cli.group()
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


#
# BUILD GROUP
#
@cli.group()
@click.pass_context
def build(ctx):
    """Build management"""
    ctx.obj = Build(ctx.obj['CONFIG'])

@build.command()
@click.pass_context
def help(ctx):
    """Print build command help"""
    click.echo(ctx.parent.get_help())


#
# DOCUMENT GROUP
#
@cli.group()
@click.pass_context
def docs(ctx):
    """Document management"""
    ctx.obj = Docs(ctx.obj['CONFIG'])

@docs.command()
@click.pass_context
def help(ctx):
    """Print document command help"""
    click.echo(ctx.parent.get_help())

@docs.command('show-page')
@click.argument('page')
@click.option('-f', '--format', help='Print output in specific format')
@pass_docs
def show_page(docs, page, format):
    """Show specific page"""
    click.echo(ctx.parent.get_help())


