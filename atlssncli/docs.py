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

pass_docs = click.make_pass_decorator(Docs)

#
# DOCUMENT GROUP
#


@click.group()
@click.pass_context
def docs(ctx):
    """Document management"""
    ctx.obj = Docs(ctx.obj['CONFIG'])


@docs.command()
@click.pass_context
def help(ctx):
    """Print document command help"""
    click.echo(ctx.parent.get_help())


@docs.command('list-spaces')
@pass_docs
def list_spaces(docs, page, format):
    """List existing spaces"""
    click.echo(ctx.parent.get_help())


@docs.command('create-space')
@click.argument('space')
@pass_docs
def create_space(docs, space):
    """Create new space"""
    click.echo(ctx.parent.get_help())


@docs.command('delete-space')
@click.argument('space')
@pass_docs
def delete_space(docs, space):
    """Delete existing space"""
    click.echo(ctx.parent.get_help())


@docs.command('show-page')
@click.argument('page')
@click.option('-f', '--format', help='Print output in specific format')
@pass_docs
def show_page(docs, page, format):
    """Show specific page"""
    click.echo(ctx.parent.get_help())
