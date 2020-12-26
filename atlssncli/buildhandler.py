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
import json
import requests

from humanfriendly.tables import format_pretty_table
from requests.auth import HTTPBasicAuth

from .cached import get_bamboo_plan_shortname
from .config import Config
from .commandhandler import CommandHandler
from .querybuilder import QueryBuilder
from .rest.bambooclient import BambooClient
from .gitcontext import get_branch, get_repo_name


class BuildHandler(CommandHandler):
    def __init__(self, config):
        super(BuildHandler, self).__init__(config)
        self.client = BambooClient(config.get_endpoint("bamboo"))
        self.client._set_auth(HTTPBasicAuth(*config.get_auth()))
        pass

    def get_project_plans(self, project):
        """Show project build plans."""
        LOG.debug("Getting project build plans: %s", project)

        res = self.client.get_project(project)

        if "components" not in res:
            res["components"] = []

        column_names = ["ID", "Name"]
        components = []
        for component in res["components"]:
            components.append([component["id"], component["name"]])

        click.echo(format_pretty_table(components, column_names))

    def get_build_queue(self):
        """Show build queue."""
        LOG.debug("Getting Bamboo build queue")

        res = self.client.get_queue("queuedBuilds")

        column_names = ["Key", "Name", "Build #", "Reason"]
        builds = []
        for build in res:
            plan_key = build["planKey"]
            plan_name = get_bamboo_plan_shortname(self.client, plan_key)
            builds.append(
                [
                    plan_key,
                    plan_name,
                    build["buildNumber"],
                    build["triggerReason"],
                ]
            )

        click.echo(format_pretty_table(builds, column_names))

    def build_plan(self, plan_id):
        """Schedule plan build."""
        LOG.debug("Queuing build plan: %s" % (plan_id))

        res = self.client.build_plan(plan_id)

        build_link = res["link"]["href"]
        build_plan_key = res["planKey"]
        build_number = res["buildNumber"]

        click.echo(
            "Scheduled build %d for %s at: %s"
            % (build_number, build_plan_key, build_link)
        )

    def enable_plan_branch(self, branch_plan_id, branch):
        """Enable plan branch"""
        if not branch_plan_id:
            # Find repositories based on current Git repository and branch
            repo = get_repo_name()

            master_plan_ids = self.config.get_repo_plan_ids(repo)
            if len(master_plan_ids) > 1:
                click.echo(
                    "ERROR: Ambiguous plan ids for repository %s repo: %s",
                    repo,
                    str(master_plan_ids),
                )
                return

            plan_id = master_plan_ids[0]

            if not branch:
                branch = get_branch()
            branch_name = branch.replace("/", "-")

            branch_plan_id = self.get_branch_plan_id(plan_id, branch_name)

            LOG.debug("Enabling plan branch: %s", branch_plan_id)
        if not branch_plan_id:
            click.echo("ERROR: No plan branch provided")
            return

        LOG.debug(
            "Enabling plan %s for branch %s with id %s",
            plan_id,
            branch,
            branch_plan_id,
        )

        plan_ref = ""
        if branch_plan_id:
            res = self.client.enable_plan(branch_plan_id)
            click.echo(
                "Enabled branch %s (%s) for plan %s"
                % (branch, branch_plan_id, plan_id)
            )
        else:
            # If the plan branch does not exist - try to create it
            res = self.client.create_plan_branch(plan_id, branch_name, branch)
            plan_ref = res["link"]["href"]
            click.echo(
                "Created new branch %s for plan %s: %s"
                % (branch, plan_id, plan_ref)
            )

    def disable_plan_branch(self, plan_id, branch):
        """Disable plan branch"""
        if not plan_id:
            # Find repositories based on current Git repository and branch
            repo = get_repo_name()

            master_plan_ids = self.config.get_repo_plan_ids(repo)
            if len(master_plan_ids) > 1:
                click.echo(
                    "ERROR: Ambiguous plan ids for repository %s repo: %s"
                    % (repo, str(master_plan_ids))
                )
                return

            plan_id = master_plan_ids[0]

        if not plan_id:
            click.echo("ERROR: No plan provided")
            return

        if not branch:
            branch = get_branch()
        branch_name = branch.replace("/", "-")

        branch_plan_id = self.get_branch_plan_id(plan_id, branch_name)

        if not branch_plan_id:
            click.echo("ERROR: Branch doesn't exist")
            return

        LOG.debug("Disabling plan %s for branch %s", plan_id, branch)

        res = self.client.disable_plan(branch_plan_id)

        click.echo(
            "Disabled branch %s (%s) for plan %s"
            % (branch, branch_plan_id, plan_id)
        )

    def get_branch_plan_id(self, plan_id, branch_name):
        plan_branches = self.client.get_plan_branches(plan_id)

        branch_plan_id = ""
        for plan_branch in plan_branches:
            if plan_branch["shortName"] == branch_name:
                branch_plan_id = plan_branch["key"]
        return branch_plan_id

    def list_plan_branches(self, plan_id):
        """List plan branches"""
        LOG.debug("Getting list of branches for plan: %s", str(plan_id))

        if not plan_id:
            repo = get_repo_name()
            master_plan_ids = self.config.get_repo_plan_ids(repo)

            if len(master_plan_ids) == 0:
                click.echo("ERROR: Please provide plan id for %s" % (repo))
                return

            if len(master_plan_ids) > 1:
                click.echo(
                    """ERROR: Multiple plan ids defined for %s.
                    Please provide specific plan id."""
                    % (repo)
                )

            plan_id = master_plan_ids[0]

        plan_branches = self.client.get_plan_branches(plan_id)

        column_names = ["Plan ID", "Branch name", "Enabled"]
        results = []

        for plan_branch in plan_branches:
            results.append(
                [
                    plan_branch["key"],
                    plan_branch["shortName"],
                    plan_branch["enabled"],
                ]
            )

        click.echo(format_pretty_table(results, column_names))

    def get_plan_status(self, plan_ids, branch):
        """Show build plans status"""
        LOG.debug("Getting information on build plans: %s", str(plan_ids))

        if not plan_ids:
            # Find repositories based on current Git repository and branch
            repo = get_repo_name()
            if not branch:
                branch = get_branch()
            branch = branch.replace("/", "-")

            master_plan_ids = self.config.get_repo_plan_ids(repo)
            if branch == "develop":
                plan_ids = master_plan_ids
            else:
                plan_ids = []
                for master_plan_id in master_plan_ids:
                    plan_branches = self.client.get_plan_branches(
                        master_plan_id
                    )
                    for plan_branch in plan_branches:
                        if plan_branch["shortName"] == branch:
                            plan_ids.append(plan_branch["key"])

        if not plan_ids:
            click.echo("ERROR: No plan for branch: {}".format(branch))
            return

        column_names = ["Plan ID", "Plan name", "Status", "Last", "Link"]
        results = []
        for plan_id in plan_ids:
            LOG.debug("Getting plan status and information for: %s", plan_id)
            plan = self.client.get_plan(plan_id)

            if plan["isBuilding"]:
                status = "Building..."
            elif plan["isActive"]:
                status = "Queued..."
            else:
                status = "Finished"
            LOG.debug("Getting plan results for plan: %s", plan_id)
            plan_results = self.client.get_plan_results(plan_id)

            # for result in plan_results:
            plan_name = get_bamboo_plan_shortname(self.client, plan_id)

            if plan_results["results"]["result"]:
                last_result = plan_results["results"]["result"][0]
                results.append(
                    [
                        plan_id,
                        plan_name,
                        status,
                        last_result["state"],
                        "https://bamboo.onedata.org/browse/{}".format(
                            last_result["key"]
                        ),
                    ]
                )
            else:
                results.append([plan_id, plan_name, "Never built", "-", "-"])

        click.echo(format_pretty_table(results, column_names))

    def list_plan_artifacts(self, plan_id):
        """List plan artifacts"""
        LOG.debug("Getting list of artifacts for plan: %s", str(plan_id))

        if not plan_id:
            repo = get_repo_name()
            master_plan_ids = self.config.get_repo_plan_ids(repo)

            if len(master_plan_ids) == 0:
                click.echo("ERROR: Please provide plan id for %s", repo)
                return

            if len(master_plan_ids) > 1:
                click.echo(
                    """ERROR: Multiple plan ids defined for %s.
                    Please provide specific plan id.""",
                    repo,
                )

            plan_id = master_plan_ids[0]

        plan_artifacts = self.client.get_plan_artifacts(plan_id)

        column_names = ["Artifact ID", "Location", "Name", "Pattern", "Shared"]
        results = []

        for artifact in plan_artifacts:
            results.append(
                [
                    artifact["id"],
                    artifact["location"],
                    artifact["name"],
                    artifact["copyPattern"],
                    artifact["shared"],
                ]
            )

        click.echo(format_pretty_table(results, column_names))

    def get_build_results(self, issue_id, favourite):
        """List plan artifacts"""
        LOG.debug("Getting list of build results for issue: %s", str(issue_id))

        build_results = self.client.get_build_results(issue_id, favourite)

        column_names = ["Plan ID", "Parent plan", "Plan name", "State"]
        results = []

        for result in build_results:
            results.append(
                [
                    result["key"],
                    result["plan"]["key"],
                    result["plan"]["shortName"],
                    result["buildState"],
                ]
            )

        click.echo(format_pretty_table(results, column_names))
