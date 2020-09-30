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

from .commandgroup import *
from .infohandler import InfoHandler

pass_info = click.make_pass_decorator(Info)

#
# INFO GROUP
#


@click.group()
@click.pass_context
def info(ctx):
    """Show information about configured Atlassian services"""
    ctx.obj = Info(ctx.obj['CONFIG'])


@info.command()
@click.pass_context
def help(ctx):
    """Print info command help"""
    click.echo(ctx.parent.get_help())


@info.command()
@pass_info
def jira(info):
    """Show information about JIRA service"""
    try:
        handler = InfoHandler(info.get_config())
        handler.show_jira_info()
    except Exception as e:
        raise click.ClickException(e.message)


@info.command()
@pass_info
def bamboo(info):
    """Show information about Bamboo service"""
    try:
        handler = InfoHandler(info.get_config())
        handler.show_bamboo_info()
    except Exception as e:
        raise click.ClickException(e.message)
