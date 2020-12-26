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
# limitations under the License.import requests

import logging as LOG
import json

from decorest import DELETE, GET, POST, PUT, query, RestClient, content, accept, on


class BambooClient(RestClient):
    """Bamboo REST client"""

    def __init__(self, endpoint):
        super(BambooClient, self).__init__(endpoint)

    @GET('info')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_info(self):
        """Get Bamboo server info"""

    @GET('agent')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_agents(self):
        """Get Bamboo plans"""

    @GET('queue')
    @query('expand')
    @query('max_result', 'max-result')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['queuedBuilds']['queuedBuild'])
    def get_queue(self, expand='queuedBuilds', max_result=500):
        """Get Bamboo build queue"""

    @GET('plan')
    @query('expand')
    @query('max_result', 'max-result')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['plans']['plan'])
    def get_plans(self, expand='plans', max_result=500):
        """Get Bamboo plans"""

    @GET('plan/{plan_id}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_plan(self, plan_id):
        """Get Bamboo plan"""

    @GET('plan/{plan_id}/label')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: [l.values()[0] for l in r.json()['labels']['label']])
    def get_plan_labels(self, plan_id):
        """Get Bamboo plan labels"""

    @GET('plan/{plan_id}/branch')
    @query('max_result', 'max-result')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['branches']['branch'])
    def get_plan_branches(self, plan_id, max_result=500):
        """Get Bamboo plan branches"""

    @GET('result')
    @query('max_results', 'max-results')
    @query('issue_id', 'issueKey')
    @query('favourite')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['results']['result'])
    def get_build_results(self, issue_id, favourite, max_results=500):
        """Get Bamboo plan branches"""

    @GET('plan/{plan_id}/artifact')
    @query('max_result', 'max-result')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['artifacts']['artifact'])
    def get_plan_artifacts(self, plan_id, max_result=500):
        """Get Bamboo plan artifacts"""

    @GET('result/{plan_id}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_plan_results(self, plan_id):
        """Get Bamboo plan build results"""

    @POST('queue/{plan_id}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def build_plan(self, plan_id):
        """Schedule plan build"""

    @PUT('plan/{plan_id}/branch/{branch_name}')
    @query('vcs_branch', 'vcsBranch')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def create_plan_branch(self, plan_id, branch_name, vcs_branch):
        """Enable plan branch"""

    @POST('plan/{plan_id}/enable')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def enable_plan(self, plan_id):
        """Enable plan branch"""

    @DELETE('plan/{plan_id}/enable')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def disable_plan(self, plan_id):
        """Disable plan branch"""