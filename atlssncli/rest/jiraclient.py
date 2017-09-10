import requests
import logging as LOG
import json

from restclient import *

class JiraClient(RestClient):
    """JIRA REST client"""

    def __init__(self, endpoint, auth):
        super(JiraClient, self).__init__(endpoint, auth)
        pass

    @GET('project')
    def get_all_projects(self):
        """Get all projects.
        """

    @GET('serverInfo')
    def get_info(self):
        """Get JIRA server info"""


    # TODO Add POST decorator
    def create_project(self, project):
        """Create new project.
        """
        req = self.build_request(['project'])
        LOG.debug('REQUEST: POST %s', req)
        #r = requests.post(req, data=project)
        #r.raise_for_status()
        #return r.json()
        return {}

    # TODO Add PUT decorator
    def update_project(self, project):
        """Update project.
        """
        req = self.build_request(['project', project['key']])
        LOG.debug('REQUEST: PUT %s', req)
        #r = requests.post(req, data=project)
        #r.raise_for_status()
        #return r.json()
        return {}

    @GET('project/{project_id}')
    def get_project(self, project_id):
        """Get project details.
        """

    @GET('project/{issue}')
    def get_issue(self, issue):
        """
        Get specific JIRA issue
        """


