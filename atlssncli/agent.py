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

from .commandgroup import Agent
from .agenthandler import AgentHandler

pass_agent = click.make_pass_decorator(Agent)

#
# AGENT GROUP
#

# attlsn agent list


@click.group()
@click.pass_context
def agent(ctx):
    """Agent management"""
    ctx.obj = Agent(ctx.obj["CONFIG"])


@agent.command()
@click.pass_context
def help(ctx):
    """Print agent command help"""
    click.echo(ctx.parent.get_help())


@agent.command()
@pass_agent
def list(agent):
    """Get agent list."""

    LOG.debug("Getting agent list")

    try:
        handler = AgentHandler(agent.get_config())
        handler.get_agent_list()
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get agent list failed")
