import click
from commandgroup import *

pass_git = click.make_pass_decorator(Git)

#
# GIT GROUP
#
@click.group()
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


