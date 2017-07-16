import requests
import logging as LOG
import json

from restclient import RestClient

class JiraClient(RestClient):
    """JIRA REST client"""

    def __init__(self, endpoint, auth):
        super(JiraClient, self).__init__(endpoint, auth) 
        pass

    def get_all_projects(self):
        """Get all projects.
        """
        req = self.build_request(['project'])
        LOG.debug('REQUEST: GET %s', req)
        r = requests.get(req, auth=self.auth)
        r.raise_for_status()
        return r.json()

    def create_project(self, project):
        """Create new project.
        """
        req = self.build_request(['project'])
        LOG.debug('REQUEST: POST %s', req)
        #r = requests.post(req, data=project)
        #r.raise_for_status()
        #return r.json()
        return {}

    def update_project(self, project):
        """Update project.
        """
        req = self.build_request(['project', project['key']])
        LOG.debug('REQUEST: PUT %s', req)
        #r = requests.post(req, data=project)
        #r.raise_for_status()
        #return r.json()
        return {}

    def get_project(self, project_id):
        """Get project details.
        """
        req = self.build_request(['project', project_id])
        LOG.debug('REQUEST: GET %s', str(req))
        r = requests.get(req, auth=self.auth)
        r.raise_for_status()
        return r.json()



