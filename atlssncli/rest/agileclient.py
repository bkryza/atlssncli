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

from decorest import DELETE, GET, POST, query, RestClient, content, accept, on, body


class AgileClient(RestClient):
    """Agile REST client"""

    def __init__(self, endpoint):
        super(AgileClient, self).__init__(endpoint)

    @GET('board')
    @query('board_type', 'type')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['values'])
    def get_boards(self, board_type):
        """Get board list"""

    @GET('board/{board_id}')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_board(self, board_id):
        """Get board"""

    @GET('board/{board_id}/backlog')
    @query('jql')
    @query('maxResults')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json()['issues'])
    def get_board_backlog(self, board_id, jql=None, maxResults=500):
        """Get board backlog"""

    @GET('board/{board_id}/sprint')
    @query('state')
    @query('max_results', 'maxResults')
    @query('start_at', 'startAt')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: (r.json()['isLast'], r.json()['values']))
    def get_sprints(self, board_id, state='active,closed,future',
                    max_results=50, start_at=0):
        """Get sprints in a specific state."""

    @GET('board/{board_id}/version')
    @query('released')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: (r.json()['isLast'], r.json()['values']))
    def get_board_versions(self, board_id, released):
        """Get sprints in a specific state."""

    @GET('sprint/{sprint_id}')
    @query('maxResults')
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def get_sprint(self, sprint_id, maxResults=500):
        """Get sprint status."""

    @POST('sprint')
    @content('application/json')
    @accept('application/json')
    @body('sprint', lambda s: json.dumps(s))
    @on(201, lambda r: r.json())
    def create_sprint(self, sprint):
        """Create sprint."""

    @DELETE('sprint/{sprint_id}')
    @content('application/json')
    @accept('application/json')
    def delete_sprint(self, sprint_id):
        """Delete sprint."""

    @GET('sprint/{sprint_id}/issue')
    @query('jql')
    @query('start_at', 'startAt')
    @query('max_results', 'maxResults')
    @content('application/json')
    @accept('application/json')
    # @on(200, lambda r: (r.json()['total'] < r.json()['maxResults'], r.json()['issues']))
    @on(200, lambda r: r.json())
    def get_sprint_issues(self, sprint_id, jql, start_at=0, max_results=500):
        """Get sprint status"""

    @POST('sprint/{sprint_id}')
    @body('sprint', lambda p: json.dumps(p))
    @content('application/json')
    @accept('application/json')
    @on(200, lambda r: r.json())
    def update_sprint(self, sprint_id, sprint={}):
        """Update sprint"""
