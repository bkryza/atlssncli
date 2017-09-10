import requests
import logging as LOG
import json

from restclient import *

class BambooClient(RestClient):
    """Bamboo REST client"""

    def __init__(self, endpoint, auth):
        super(BambooClient, self).__init__(endpoint, auth)
        pass

    @GET('info')
    def get_info(self):
        """Get Bamboo server info"""


