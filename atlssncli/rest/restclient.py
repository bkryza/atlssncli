import urlparse
import logging as LOG
import requests

try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode


class RestClient(object):
    """Simple REST client"""

    def __init__(self, endpoint, auth):
        self.endpoint = endpoint
        if not self.endpoint.endswith("/"):
            self.endpoint = self.endpoint + "/"
        self.auth = auth
        pass

    def build_request(self, path_components = [], query_components = {}):
        """Builds request by combining the endpoint with path 
        and query components.
        """
        LOG.debug("Building request from path tokens: %s", path_components)

        req = urlparse.urljoin(self.endpoint, "/".join(path_components))
        if not query_components == None and len(query_components)>0:
            req += "?" + urlencode(query_components)

        return req
