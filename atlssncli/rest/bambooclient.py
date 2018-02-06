import requests
import logging as LOG
import json

from restclient import GET, POST, query, RestClient


class BambooClient(RestClient):
    """Bamboo REST client"""

    def __init__(self, endpoint, auth):
        super(BambooClient, self).__init__(endpoint, auth)

    @GET('info')
    def get_info(self):
        """Get Bamboo server info"""

    @GET('queue')
    @query('expand', 'queuedBuilds')
    def get_queue(self):
        """Get Bamboo build queue"""

    @POST('queue/{plan_id}')
    def build_plan(self, plan_id):
        """Schedule plan build"""
