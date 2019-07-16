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
from commandgroup import *
from sprinthandler import SprintHandler
import logging as LOG
import traceback


pass_sprint = click.make_pass_decorator(Sprint)

#
# SPRINT GROUP
#

# attlsn board list
# attlsn board select 7
# attlsn board backlog
# attlsn sprint list
# attlsn sprint list active,closed
# attlsn sprint status
# attlsn sprint status 123
# attlsn sprint start 123
# attlsn sprint close
# attlsn sprint create "Sprint 123"
# attlsn sprint rename 123 "Sprint 123 Renamed"
# attlsn sprint issues
# attlsn sprint issues --mine
# attlsn sprint issues --assignee plgkryza
# attlsn sprint issues --reporter bkryza


@click.group()
@click.pass_context
def sprint(ctx):
    """Sprint management"""
    ctx.obj = Sprint(ctx.obj['CONFIG'])


@sprint.command()
@click.pass_context
def help(ctx):
    """Print sprint command help"""
    click.echo(ctx.parent.get_help())


@sprint.command()
@click.argument('sprint_id', required=False)
@pass_sprint
def status(sprint, sprint_id):
    """
    Get sprint status.

    If no sprint id is provided, currently active sprint will be returned.
    """
    LOG.debug("Getting sprint status %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.get_sprint_status(sprint_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get sprint status failed")


@sprint.command()
@click.argument('sprint_id')
@click.argument('name')
@pass_sprint
def rename(sprint, sprint_id, name):
    """Rename specific sprint."""

    LOG.debug("Renaming sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.rename_sprint(sprint_id, name)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Sprint rename failed")


@sprint.command()
@click.argument('sprint_id')
@click.argument('start_date', required=False)
@click.argument('duration', required=False)
@pass_sprint
def start(sprint, sprint_id, start_date, duration):
    """
    Start specific sprint.

    If start_date and duration are not provided, sprint is started
    with the current time and default duration specified in config.ini.

    In order to provide duration, start_date must be also provided,
    but can be specified simply as 'now'.
    """

    LOG.debug("Starting sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.start_sprint(sprint_id, start_date, duration)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Sprint start failed")


@sprint.command()
@click.argument('sprint_id')
@pass_sprint
def stop(sprint, sprint_id):
    """Stop specific sprint."""

    LOG.debug("Renaming sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.stop_sprint(sprint_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Sprint stop failed")


@sprint.command()
@click.argument('board_id', required=False)
@click.option('--active', is_flag=True, help='Include active sprints',
              default=False)
@click.option('--closed', is_flag=True, help='Include closed sprints',
              default=False)
@click.option('--future', is_flag=True, help='Include future sprints',
              default=False)
@pass_sprint
def list(sprint, board_id, active, closed, future):
    """
    List sprints for board.

    If no board is provided on the command line, the active
    board from config.ini is used.
    """

    LOG.debug("Getting list of sprints for board %s", board_id)

    try:
        handler = SprintHandler(sprint.get_config())
        state = []
        if active:
            state.append('active')
        if closed:
            state.append('closed')
        if future:
            state.append('future')
        handler.get_sprint_list(board_id, ','.join(state))
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Listing sprints failed")


@sprint.command()
@click.argument('sprint_id', required=True)
@click.option('--open', 'opened', is_flag=True, help='Include open tickets',
              default=False)
@click.option('--closed', is_flag=True, help='Include closed tickets',
              default=False)
@click.option('--in-progress', 'in_progress', is_flag=True, help='Include in progress tickets',
              default=False)
@click.option('--resolved', is_flag=True, help='Include resolved tickets',
              default=False)
@click.option('--assignee', help='Specify assignee username')
@click.option('--jql', help='Specify custom JQL query to fileter results')
@pass_sprint
def issues(sprint, sprint_id, assignee, opened, in_progress, closed, resolved,
           jql):
    """
    List issues for sprint.
    """

    LOG.debug("Getting list of issues for sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.get_sprint_issues(
            sprint_id, assignee, opened, in_progress, closed, resolved, jql)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Listing sprint issues failed")