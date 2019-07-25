atlssncli
#################################################

.. image::	https://img.shields.io/travis/bkryza/atlssncli.svg
    :target: https://travis-ci.org/bkryza/atlssncli

.. image:: https://img.shields.io/pypi/v/atlssncli.svg
    :target: https://pypi.python.org/pypi/atlssncli

.. image:: https://img.shields.io/pypi/l/atlssncli.svg
    :target: https://pypi.python.org/pypi/atlssncli

.. image:: https://img.shields.io/pypi/pyversions/atlssncli.svg
    :target: https://pypi.python.org/pypi/atlssncli

Simple command-line client unifying access to Atlassian_ ® services.

.. role:: bash(code)
   :language: bash


.. contents::

Overview
========
atlssncli_ is a simple command-line utility written in Python
enabling easy, context-based access to various features of Atlassian®
services over REST API. The context can be specified in the configuration
file in terms of current board or project, and also is extracted
automatically from the Git branch of the current working directory.

The goal of this project is to provide a concise command-line
interface for everyday tasks involving sprint, issue and build
management. atlssncli_ focuses on simplicity over completeness,
to provide as quick as possible access to most commonly used features,
assuming that more complex can be achieved otherwise, e.g. using web
interface.


Installation
============

Configuration
=============

Usage introduction
==================

Command reference
=================

info - service information
--------------------------

Show information about JIRA service::
    atlssn info jira

Show information about Bamboo service::
    atlssn info bamboo

agent - Bamboo agents information
----------------------------------

Show information about Bamboo agents::
    atlssn agent list

project - manage projects
-------------------------

Manage projects in the Jira and Bamboo services.

List all available projects::
    atlssn project list

Select currently active project::
    atlssn project select [<project_key>]

Get information about specific project::
    atlssn project info [<project_key>]

List project components::
    atlssn project list-components [<project_key>]

List project issue types::
    atlssn project list-issue-types [<project_key>]

board - manage Jira boards
--------------------------

Get board backlog::
    atlssn board backlog [-a|--assignee <user_id>] [-q|--jql <jql_query>]

Get board list::
    atlssn board list

Set default board::
    atlssn board select <board_id>

Get board status::
    atlssn board status [<board_id>]

sprint - manage sprints
-----------------------

List all sprints or sprints in a given state::
    atlssn sprint list <--active|--future|--close>

Create sprint::
    atlssn sprint create <sprint_id>

Rename sprint::
    atlssn sprint rename <sprint_id> <new_name>

Start sprint::
    atlssn sprint start <sprint_id> [<start_date> [<duration>]]

Stop sprint::
    atlssn sprint stop <sprint_id>

Get sprint status::
    atlssn sprint status <sprint_id>

List sprint issues::
    atlssn sprint issues <sprint_id>

List sprint issues by assignee::
    atlssn sprint issues <sprint_id> --assignee johndoe

List sprint issues by status::
    atlssn sprint issues <sprint_id> --resolved --closed

License
=======

Copyright 2019 Bartosz Kryza <bkryza@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

All Atlassian® services referenced in this project are registered
trademarks of Atlassian Corporation Plc.

The author of this project is not affiliated in any way with
Atlassian Corporation Plc.

.. _Atlassian: https://www.atlassian.com/
