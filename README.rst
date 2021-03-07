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
interface or other command line clients.


Installation
============

.. code-block:: bash

	pip install atlssncli

Configuration
=============

Configuration file should be placed in `~/.atlssncli/config.ini`:

.. code-block:: bash

	[common]
	username = username
	password = password
	version = 6
	active_project = BKP

	[jira]
	endpoint = https://jira.example.com/rest/api/latest

	[agile]
	endpoint = https://jira.example.com/rest/agile/latest
	board = 7
	sprint_duration = 14

	[bamboo]
	endpoint = https://bamboo.example.com/rest/api/latest
	component1 = BKP-CMP1
	component2 = BKP-CMP2
	component3 = BKP-CMP3

Autocompletion
--------------

Bash
~~~~
Add the following line to your `~/.bashrc`:

.. code-block:: bash

    eval "$(_ATLSSN_COMPLETE=source_bash atlssn)"


Zsh
~~~
Add the following line to your `~/.zshrc`:

.. code-block:: bash

    eval "$(_ATLSSN_COMPLETE=source_zsh atlssn)"


Basic usage
===========

...

Command reference
=================

info
----

Show information about services.

Show information about JIRA® service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn info jira

Show information about Bamboo® service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn info bamboo

agent
-----

Bamboo® agents information, REST API for agents only supports a single method.

Show information about Bamboo® agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    atlssn agent list

project
-------

Manage projects in the Jira® and Bamboo® services.

List all available projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn project list

Select currently active project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn project select <project_key>

Get information about specific project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn project info [<project_key>]

List project components
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn project list-components [<project_key>]

List project issue types
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn project list-issue-types [<project_key>]

board - manage Jira® boards
---------------------------

Get board backlog
~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn board backlog [-a|--assignee <user_id>] [-q|--jql <jql_query>]

    # Examples
    atlssn board backlog -q 'status = "Open" AND assignee = "bkryza"'
    atlssn board backlog -a bkryza

Get board list
~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn board list

Set default board
~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn board select <board_id>

Get board status
~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn board status [<board_id>]

sprint - manage sprints
-----------------------
Below commands, which accept optional sprint_id,
will act on active sprint when sprint_id is not provided.

List all sprints or sprints in a given state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint list [--active|--future|--closed]

Create sprint
~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint create [-n|--name <name>]
                         [-s|--start-date YYYY-MM-DD]
                         [-d|--duration <days>]

Rename sprint
~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint rename <sprint_id> <new_name>

Start sprint
~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint start <sprint_id> [<start_date> [<duration>]]

Stop sprint
~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint stop <sprint_id>

Get sprint status
~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint status [<sprint_id>]

List sprint issues
~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint issues [<sprint_id>]

List sprint issues by assignee
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint issues [<sprint_id>] --assignee johndoe

List sprint issues by status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    atlssn sprint issues [<sprint_id>] --resolved --closed

issue - manage issues
---------------------

Get issue types for active project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    **atlssn issue types

Get issue types for specific project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    **atlssn issue types <project_id>

Create issue
~~~~~~~~~~~~
.. code-block:: bash

	**atlssn issue create <summary> [-t|--type <issue_type>]
	                              [-a|--assignee <username>]
	                              [-r|--reporter <username>]
	                              [-i|--priority <priority>]
	                              [-l|--labels <label>,<label>,...,<label>]
	                              [-d|--description <text>]
	                              [-x|--fix-versions <versions>]
	                              [-c|--components <component>,...,<component>]

Edit issue
~~~~~~~~~~
.. code-block:: bash

	**atlssn issue edit <issue_id> [-t|--type <issue_type>]
	                             [-a|--assignee <username>]
	                             [-r|--reporter <username>]
	                             [-i|--priority <priority>]
	                             [-l|--labels <label>,<label>,...,<label>]
	                             [-d|--description <text>]
	                             [-x|--fix-versions <versions>]
	                             [-c|--components <component>,...,<component>]

Get issue status
~~~~~~~~~~~~~~~~
.. code-block:: bash

		atlssn issue status <issue_id>

Assign issue
~~~~~~~~~~~~
.. code-block:: bash

		atlssn issue assign <issue_id> <username>

Get issue changelog
~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue changelog <issue_id>

Add issue comment
~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue comment <issue_id> <comment>

Change issue state
~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue update <issue_id> <comment>

Link issues
~~~~~~~~~~~
.. code-block:: bash

    **atlssn issue link <issue_id> <outward_issue_id>

List issue attachments
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    **atlssn issue attachments <issue_id>

Add issue attachment
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue attach <issue_id> <file_path>

Delete issue attachment
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue detach <issue_id> <file_name>

List possible issue transitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue transitions <issue_id>

Transition issue to different state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue transition <issue_id> <state_name>

List possible issue resolutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue resolutions <issue_id>

Resolve issue
~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue resolve <issue_id> <resolution>

Create branch from issue
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue branch <issue_id> <state_name>

List Git branches for issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

		**atlssn issue branches <issue_id>



TODO
====

* Refactor output formatting to enable custom formatters
* Add OAuth support
* Move todo's to GitHub issues

License
=======

Copyright 2019-present Bartosz Kryza <bkryza@gmail.com>

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
