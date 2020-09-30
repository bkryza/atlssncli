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

from decorest import RestClient, GET, POST, PUT, DELETE, body,\
                     content, accept, query, on


class JiraClient(RestClient):
    """JIRA REST client"""

    def __init__(self, endpoint):
        super(JiraClient, self).__init__(endpoint)
        pass

    @GET('project')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_all_projects(self):
        """Get all projects.
        """

    @GET('issue/createmeta')
    @query('project_id', 'projectKeys')
    @query('max_results', 'maxResults')
    @query('start_at', 'startAt')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['projects'][0]['issuetypes'])
    def get_issue_types(self, project_id):
        """Get issue types for project."""

    @GET('resolution')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_resolutions(self):
        """Get issue resolutions."""

    @GET('serverInfo')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_info(self):
        """Get JIRA server info"""

    # TODO Add POST decorator
    def create_project(self, project):
        """Create new project.
        """
        # req = self.build_request(['project'])
        # LOG.debug('REQUEST: POST %s', req)
        #r = requests.post(req, data=project)
        # r.raise_for_status()
        # return r.json()
        return {}

    # TODO Add PUT decorator
    def update_project(self, project):
        """Update project.
        """
        # req = self.build_request(['project', project['key']])
        # LOG.debug('REQUEST: PUT %s', req)
        #r = requests.post(req, data=project)
            # r.raise_for_status()
        # return r.json()
        return {}

    @GET('project/{project_id}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_project(self, project_id):
        """Get project details.
        """

    @GET('issue/{issue}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_issue(self, issue):
        """
        Get specific JIRA issue
        """

    @PUT('issue/{issue}/assignee')
    @content('application/json')
    @accept('application/json')
    @body('data', lambda s: json.dumps(s))
    @on(200, lambda r: r.json())
    def assign_issue(self, issue, data):
        """
        Assign JIRA issue
        """
