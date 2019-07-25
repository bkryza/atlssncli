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
import pdb
import sys

from commandgroup import *
from projecthandler import ProjectHandler

pass_project = click.make_pass_decorator(Project)

#
# PROJECT GROUP
#


@click.group()
@click.pass_context
def project(ctx):
    """Manage projects"""
    ctx.obj = Project(ctx.obj['CONFIG'])


@project.command()
@click.pass_context
def help(ctx):
    """Print project command help"""
    click.echo(ctx.parent.get_help())


@project.command()
@pass_project
def list(project):
    """List all projects"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.list_projects()
    except Exception as e:
        raise click.ClickException(e.message)


@project.command()
@click.argument('project_id', 'Project id or key.', required=False)
@pass_project
def info(project, project_id):
    """Get project details"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_details(project_id)
    except Exception as e:
        raise click.ClickException(e.message)


@project.command('list-components')
@click.argument('project_id', 'Project id or key.', required=False)
@pass_project
def list_components(project, project_id):
    """List project components"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_components(project_id)
    except Exception as e:
        raise click.ClickException(e.message)


@project.command('list-issue-types')
@click.argument('project_id', 'Project id or key.', required=False)
@pass_project
def list_issue_types(project, project_id):
    """List project issue types"""
    try:
        handler = ProjectHandler(project.get_config())
        handler.get_project_issue_types(project_id)
    except Exception as e:
        raise click.ClickException(e.message)


@project.command()
@click.argument('project_id', required=False)
@pass_project
def select(project, project_id):
    """Select active project

       All consecutive commands will be performed in the scope of that project.
    """
    try:
        handler = ProjectHandler(project.get_config())
        handler.select_project(project_id)
    except Exception as e:
        raise click.ClickException(e)
