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

from .commandgroup import Board
from .boardhandler import BoardHandler

pass_board = click.make_pass_decorator(Board)

#
# BOARD GROUP
#


@click.group()
@click.pass_context
def board(ctx):
    """Board management"""
    ctx.obj = Board(ctx.obj["CONFIG"])


@board.command()
@click.pass_context
def help(ctx):
    """Print board command help."""
    click.echo(ctx.parent.get_help())


@board.command()
@click.argument("board_id", required=True)
@pass_board
def select(board, board_id):
    """
    Set default board.

    After this operation, all board commands will by default be
    executed against this board.
    """
    LOG.debug("Setting default %s", board_id)

    try:
        board.get_config().set_board(board_id)
        click.echo("Active board: %s" % (board_id))
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Set default board failed")


@board.command()
@click.option(
    "--scrum", is_flag=True, help="Include scrum boards", default=False
)
@click.option(
    "--kanban", is_flag=True, help="Include kanban boards", default=False
)
@pass_board
def list(board, scrum, kanban):
    """Get board list."""
    LOG.debug("Getting board list.")

    try:
        handler = BoardHandler(board.get_config())
        board_type = []
        if scrum:
            board_type.append("scrum")
        if kanban:
            board_type.append("kanban")
        if not scrum and not kanban:
            board_type = ["scrum", "kanban"]
        handler.get_board_list(",".join(board_type))
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get sprint status failed")


@board.command()
@click.option("-b", "--board", "board_id", required=False)
@pass_board
def status(board, board_id):
    """
    Get board status.

    If no board id is provided, active board from config.ini will be used.
    """
    LOG.debug("Getting board status %s", board_id)

    try:
        handler = BoardHandler(board.get_config())
        handler.get_board_status(board_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get board status failed")


@board.command()
@click.argument("board_id", required=False)
@click.option("-a", "--assignee", help="Specify assignee username.")
@click.option("-q", "--jql", help="JQL query.", required=False)
@pass_board
def backlog(board, board_id, assignee, jql):
    """
    Get board backlog.

    If no board id is provided, active board from config.ini will be used.
    """
    LOG.debug("Getting board status %s", board_id)

    try:
        handler = BoardHandler(board.get_config())
        handler.get_board_backlog(board_id, assignee, jql)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get board status failed")


@board.command()
@click.argument("board_id", required=False)
@click.option(
    "-r", "--released", is_flag=True, help="List only release versions."
)
@pass_board
def version(board, board_id, released):
    """Get release versions associated with the board."""
    LOG.debug("Getting board versions %s", board_id)

    try:
        handler = BoardHandler(board.get_config())
        handler.get_board_versions(board_id, released)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get board status failed")
