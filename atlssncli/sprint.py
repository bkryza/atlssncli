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
from .sprinthandler import SprintHandler

pass_sprint = click.make_pass_decorator(Sprint)

#
# SPRINT GROUP
#

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
@click.argument('board_id', required=False)
@click.option('-n', '--name', required=False)
@click.option('-s', '--start-date', 'start_date', required=False)
@click.option('-d', '--duration', required=False)
@pass_sprint
def create(sprint, board_id, name, start_date, duration):
    """
    Create new sprint.

    If no board id is provided, it will be taken from the config.ini.
    """

    LOG.debug("Creating new sprint on board %s", board_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.create_sprint(board_id, name, start_date, duration)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Creating sprint failed")


@sprint.command()
@click.argument('sprint_id')
@pass_sprint
def delete(sprint, sprint_id):
    """Delete specific sprint."""

    LOG.debug("Deleting sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.delete_sprint(sprint_id)
        click.echo("Sprint {} deleted successfully".format(sprint_id,))
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Sprint delete failed")


@sprint.command()
@click.argument('sprint_id', required=False)
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
@click.option('-s', '--start-date', 'start_date', required=False)
@click.option('-d', '--duration', required=False)
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
@click.argument('sprint_id', required=False)
@pass_sprint
def close(sprint, sprint_id):
    """Close specific sprint."""

    LOG.debug("Closing sprint %s", sprint_id)

    try:
        handler = SprintHandler(sprint.get_config())
        handler.close_sprint(sprint_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Sprint closing failed")


@sprint.command()
@click.argument('board_id', required=False)
@click.option('-a', '--active', is_flag=True, help='Include active sprints',
              default=False)
@click.option('-c', '--closed', is_flag=True, help='Include closed sprints',
              default=False)
@click.option('-f', '--future', is_flag=True, help='Include future sprints',
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
@click.argument('sprint_id', required=False)
@click.option('-o', '--open', 'opened', is_flag=True,
              help='Include open tickets', default=False)
@click.option('-c', '--closed', is_flag=True, help='Include closed tickets',
              default=False)
@click.option('-p', '--in-progress', 'in_progress', is_flag=True,
              help='Include in progress tickets', default=False)
@click.option('-r', '--resolved', is_flag=True, help='Include resolved tickets',
              default=False)
@click.option('-a', '--assignee', help='Specify assignee username')
@click.option('-q', '--jql', help='Specify custom JQL query to fileter results')
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
