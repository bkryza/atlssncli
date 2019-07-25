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
from buildhandler import BuildHandler
import logging as LOG
import traceback


pass_build = click.make_pass_decorator(Build)

#
# BUILD GROUP
#

@click.group()
@click.pass_context
def build(ctx):
    """Build management"""
    ctx.obj = Build(ctx.obj['CONFIG'])


@build.command()
@click.pass_context
def help(ctx):
    """Print build command help."""
    click.echo(ctx.parent.get_help())


@build.command()
@click.argument('plan_id')
@pass_build
def run(build, plan_id):
    """Add plan to build queue."""
    LOG.debug("Adding plan to build queue %s", plan_id)
    try:
        handler = BuildHandler(build.get_config())
        handler.build_plan(plan_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get plan failed")


@build.command()
@click.argument('plan_id', required=False, nargs=-1)
@click.option('-b', '--branch', help='Branch name')
@pass_build
def enable(build, plan_id, branch):
    """Enable branch for plan"""
    LOG.debug("Enabling branch %s for plan %s", branch, plan_id)
    try:
        handler = BuildHandler(build.get_config())
        handler.enable_plan(plan_id, branch)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Branch enable failed")


@build.command()
@click.argument('plan_id', required=False, nargs=-1)
@click.option('-b', '--branch', help='Branch name')
@pass_build
def disable(build, plan_id, branch):
    """Disable branch for plan."""
    LOG.debug("Disabling branch %s for plan %s", branch, plan_id)
    try:
        handler = BuildHandler(build.get_config())
        handler.disable_plan(plan_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Branch disable failed")


@build.command()
@click.argument('plan_id', required=False, nargs=-1)
@click.option('-b', '--branch', help='Branch name')
@pass_build
def status(build, plan_id, branch):
    """Get plan status."""
    LOG.debug("Getting plan status %s", plan_id)

    try:
        handler = BuildHandler(build.get_config())
        handler.get_plan_status(plan_id, branch)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Get plan status failed")


@build.command()
@pass_build
def queue(build):
    """Get current build queue."""
    try:
        handler = BuildHandler(build.get_config())
        handler.get_build_queue()
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Failed getting build queue")


@build.command('list-branches')
@click.argument('plan_id', required=False, nargs=1)
@pass_build
def list_branches(build, plan_id):
    """List branches for build plan."""
    LOG.debug("Getting plan branches %s", plan_id)

    try:
        handler = BuildHandler(build.get_config())
        handler.list_plan_branches(plan_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Listing plan branches failed")

@build.command('list-artifacts')
@click.argument('plan_id', required=False, nargs=1)
@pass_build
def list_artifacts(build, plan_id):
    """List artifacts for build plan."""
    LOG.debug("Getting plan artifacts %s", plan_id)

    try:
        handler = BuildHandler(build.get_config())
        handler.list_plan_artifacts(plan_id)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Listing plan artifacts failed")

@build.command('results')
@click.argument('issue_id', required=False, nargs=1)
@click.option('-f', '--favourite', help='Only favourite plans.', default=False,
              is_flag=True)
@pass_build
def get_results(build, issue_id, favourite):
    """Get build results."""
    LOG.debug("Getting build results for issue %s", issue_id)

    try:
        handler = BuildHandler(build.get_config())
        handler.get_build_results(issue_id, favourite)
    except Exception:
        traceback.print_exc()
        raise click.ClickException("Getting build results failed")
