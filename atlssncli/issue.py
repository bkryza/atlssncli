import click

from commandgroup import *
from projecthandler import ProjectHandler

pass_issue = click.make_pass_decorator(Issue)


#
# ISSUE GROUP
#
@click.group()
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



