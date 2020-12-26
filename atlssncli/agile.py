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

from .commandgroup import Agile

pass_agile = click.make_pass_decorator(Agile)

#
# AGILE GROUP
#


@click.group()
@click.pass_context
def agile(ctx):
    """Sprint management"""
    ctx.obj = Agile(ctx.obj["CONFIG"])


@agile.command()
@click.pass_context
def help(ctx):
    """Print agile command help"""
    click.echo(ctx.parent.get_help())


@agile.command("create-sprint")
@click.argument("sprint")
@pass_agile
def create_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command("start-sprint")
@click.argument("sprint")
@pass_agile
def create_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command("close-sprint")
@pass_agile
def close_sprint(agile):
    """Close sprint"""
    click.echo(ctx.parent.get_help())


@agile.command("delete-sprint")
@click.argument("sprint")
@pass_agile
def delete_sprint(agile, sprint):
    """Create new sprint"""
    click.echo(ctx.parent.get_help())


@agile.command("sprint-status")
@pass_agile
def sprint_status(agile):
    """Get currently active sprint status"""
    click.echo(ctx.parent.get_help())
