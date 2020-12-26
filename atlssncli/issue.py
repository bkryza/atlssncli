# -*- coding: utf-8 -*-
#
# Copyright 2019 Bartosz Kryza <bkryza@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import logging as LOG

import traceback

from .commandgroup import *
from .projecthandler import ProjectHandler
from .issuehandler import IssueHandler

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
@click.argument('project_id', required=False)
@pass_issue
def types(issue, project_id):
    """List issue types for project."""
    LOG.debug("Listing project issue types %s", project_id)

    try:
        handler = IssueHandler(issue.get_config())
        handler.get_issue_types(project_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Getting project issue types failed")


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
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
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
def edit(issue, summary, project, issue_type, assignee, reporter,
           priority, labels, estimate, description, fix_versions, duedate,
           components):
    """Edit existing issue."""
    LOG.debug("Modifying issue %s (components: %s)", summary, components)
    pass


@issue.command()
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def status(issue, issue_id):
    """Get issue"""
    LOG.debug("Get issue %s", issue_id)

    try:
        handler = IssueHandler(issue.get_config())
        handler.get_issue(issue_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Getting issue failed")


@issue.command()
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def delete(issue, issue_id):
    """Delete issue"""
    pass


@issue.command()
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@click.argument('assignee')
@pass_issue
def assign(issue, issue_id, assignee):
    """Assign issue"""
    LOG.debug("Assign issue %s to %s", issue_id, assignee)

    try:
        handler = IssueHandler(issue.get_config())
        handler.assign_issue(issue_id, assignee)
        click.echo('Assigned {} issue to {}'.format(
            issue_id, assignee))
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Assigning issue failed")


@issue.command('list-transitions')
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def transitions(issue, issue_id):
    """List possible transitions"""
    pass


@issue.command('transition')
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@click.argument('state')
@pass_issue
def transition(issue, issue_id, state):
    """Transition the issue to another state"""
    pass


@issue.command('list-votes')
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def list_votes(issue, issue_id):
    """List issue votes"""
    pass


@issue.command()
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def vote(issue, issue_id):
    """Vote for an issue"""
    pass


@issue.command()
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def unvote(issue, issue_id):
    """Unvote an issue"""
    pass


@issue.command('branch')
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@click.argument('repository')
@click.argument('branch')
@pass_issue
def branch(issue, issue_id, repository, branch):
    """Create an issue branch in repository from existing branch"""
    pass


@issue.command('branches')
@click.argument('issue_id', envvar='ATLSSNCLI_ISSUE_ID')
@pass_issue
def branches(issue, issue_id):
    """List branches created for this issue"""
    pass
