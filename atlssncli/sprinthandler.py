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

import requests
import click
import logging as LOG
import json
from datetime import datetime, timedelta
from humanfriendly.tables import format_pretty_table
from requests.auth import HTTPBasicAuth
from dateutil.parser import parse

from .config import Config
from .commandhandler import CommandHandler
from .rest.agileclient import AgileClient


class SprintHandler(CommandHandler):
    def __init__(self, config):
        super(SprintHandler, self).__init__(config)
        self.client = AgileClient(config.get_endpoint("agile"))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))

    def get_sprint_status(self, sprint_id):
        """Show sprint status."""
        LOG.debug("Getting sprint status: %s", sprint_id)

        if not sprint_id:
            sprint_id = self._get_active_sprint()

        res = self.client.get_sprint(sprint_id)

        self._render_sprint_list([res])

    def get_sprint_list(self, board_id=None, state="active,closed,future"):
        """Show sprint list."""
        if not board_id:
            board_id = self.config.get_board()
            if not board_id:
                LOG.error("Cannot list sprints without board id")
                raise "Cannot list sprints without board id"

        LOG.debug("Getting sprint list for board: %s", board_id)

        is_last = False
        start_at = 0
        res = []
        while not is_last:
            is_last, chunk = self.client.get_sprints(
                board_id, state, 50, start_at
            )
            res.extend(chunk)
            start_at += len(chunk)

        self._render_sprint_list(res)

    def create_sprint(self, board_id, name, start_date, duration):
        """Create new sprint."""
        if not board_id:
            board_id = self.config.get_board()
            if not board_id:
                LOG.error("Cannot create sprint without board id")
                raise "Cannot create sprint without id"

        LOG.debug("Creating sprint on board: %s", board_id)

        sprint = {}
        sprint["originBoardId"] = board_id
        if name:
            sprint["name"] = name

        if not start_date or start_date == "now":
            start_date = datetime.now()

        if not duration:
            duration = self.config.get_sprint_duration()

        end_date = start_date + timedelta(days=int(duration))

        sprint["startDate"] = start_date.isoformat()
        sprint["endDate"] = end_date.isoformat()

        res = self.client.create_sprint(sprint)

        print(str(res))

        self._render_sprint_list([res])

    def delete_sprint(self, sprint_id):
        """Delete sprint."""
        LOG.debug("Deleting sprint: %s", sprint_id)

        self.client.delete_sprint(sprint_id)

    def rename_sprint(self, sprint_id, name):
        """Rename selected sprint."""
        if not sprint_id:
            sprint_id = self._get_active_sprint()

        LOG.debug("Renaming sprint %s to %s", sprint_id, name)

        res = self.client.update_sprint(sprint_id, {"name": name})

        self._render_sprint_list([res])

    def start_sprint(self, sprint_id, start_date=None, duration=None):
        """
        Start selected sprint.

        By default the sprint will be started for duration specified in
        the config.ini with start date set to now.
        """
        LOG.debug("Starting sprint %s", sprint_id)

        sprint = {}
        sprint["state"] = "active"

        if not start_date or start_date == "now":
            start_date = datetime.now()

        if not duration:
            duration = self.config.get_sprint_duration()

        end_date = start_date + timedelta(days=int(duration))

        sprint["startDate"] = start_date.isoformat()
        sprint["endDate"] = end_date.isoformat()

        res = self.client.update_sprint(sprint_id, sprint)

        self._render_sprint_list([res])

    def close_sprint(self, sprint_id):
        """Close selected sprint."""
        if not sprint_id:
            sprint_id = self._get_active_sprint()

        LOG.debug("Closing sprint %s", sprint_id)

        sprint = {}
        sprint["state"] = "closed"

        res = self.client.update_sprint(sprint_id, sprint)

        self._render_sprint_list([res])

    def get_sprint_issues(
        self,
        sprint_id,
        assignee,
        status_open,
        status_in_progress,
        status_closed,
        status_resolved,
        jql,
    ):
        """Get sprint issues."""
        if not sprint_id:
            sprint_id = self._get_active_sprint()

        LOG.debug("Getting sprint %s issues", sprint_id)

        query = []
        query_str = ""

        if status_open:
            query.append("Open")

        if status_in_progress:
            query.append("'In progress'")

        if status_closed:
            query.append("Closed")

        if status_resolved:
            query.append("Resolved")

        if query:
            query_str = "status in (" + ",".join(query) + ")"

        if assignee:
            if query:
                query_str += " AND "
            query_str += "assignee={}".format(
                assignee,
            )

        if not jql:
            jql = query_str

        is_last = False
        start_at = 0
        res = []
        while not is_last:
            chunk = self.client.get_sprint_issues(sprint_id, jql, start_at, 50)

            res.extend(chunk["issues"])
            start_at += len(chunk["issues"])
            is_last = chunk["total"] == len(res)

        self._render_sprint_issues(res)

    def _get_active_sprint(self):
        """Get active sprint."""
        board_id = self.config.get_board()
        if not board_id:
            LOG.error("Cannot determine active sprint without board id")
            raise "Cannot determine active sprint without board id"

        LOG.debug("No sprint provided - getting active sprint id...")

        # TODO: decorest doesn't seem to handle specifying only one out
        # of multiple default arguments
        is_last, res = self.client.get_sprints(board_id, "active", 50, 0)
        if not res:
            raise Exception(
                "Cannot get active sprint for board: {}".format(str(board_id))
            )
        if len(res) > 1:
            raise Exception(
                "Multiple sprints are currently active - \
                 please specify the sprint id manually..."
            )

        sprint_id = res[0]["id"]

        LOG.debug("Found active sprint id: %s", sprint_id)

        return sprint_id

    def _render_sprint_list(self, sprints):
        """Render sprint list."""

        column_names = ["ID", "Name", "State", "Start", "End", "Board"]
        values = []
        for sprint in sprints:
            if "startDate" in sprint:
                start_date = parse(sprint["startDate"]).date()
            if "endDate" in sprint:
                end_date = parse(sprint["endDate"]).date()
            else:
                start_date = "-"
                end_date = "-"
            try:
                board_id = str(sprint["originBoardId"])
            except:
                board_id = "-"
            values.append(
                [
                    str(sprint["id"]),
                    sprint["name"],
                    sprint["state"],
                    str(start_date),
                    str(end_date),
                    board_id,
                ]
            )

        click.echo(format_pretty_table(values, column_names))

    def _render_sprint_issues(self, issues):
        """Render sprint issues."""

        column_names = [
            "ID",
            "Key",
            "Summary",
            "Status",
            "Assignee",
            "Progress",
        ]
        values = []
        for issue in issues:
            values.append(
                [
                    str(issue["id"]),
                    str(issue["key"]),
                    str(issue["fields"]["summary"]),
                    str(issue["fields"]["status"]["name"]),
                    str(issue["fields"]["assignee"]["key"]),
                    str(issue["fields"]["progress"]["progress"]),
                ]
            )

        click.echo(format_pretty_table(values, column_names))
