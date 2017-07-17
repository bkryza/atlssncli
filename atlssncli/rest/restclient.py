import urlparse
import logging as LOG
import requests
import re
import inspect

try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode

def dict_from_args(func, *args):
    """
    Convert function arguments to a dictionary
    """
    result = {}
    args_name = inspect.getargspec(func)[0]
    for i in range(len(args)):
        result[args_name[i]] = args[i]

    return result


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def render_path(path, args):
    """Render REST path from *args
    """
    LOG.debug('RENDERING PATH FROM: %s,  %s', path, args)
    result = path
    matches = re.search(r'{(.*)}', result)
    while matches:
        path_token = matches.group(1)
        if not path_token in args:
            raise Exception("Missing argument %s in REST call"%(path_token))
        result = re.sub('{%s}'%(path_token), args[path_token], result)
        matches = re.search(r'{(.*)}', result)
    return result


class GET(object):
    def __init__(self, path):
        self.path_template = path

    def __call__(self, func):
        def get_decorator(*args):
            rest_client = args[0]
            req_path = render_path(self.path_template, dict_from_args(func, *args))
            query_parameters = None

            try:
                query_parameters = func._query__parameters
            except:
                pass

            req = rest_client.build_request(req_path.split('/'), query_parameters)

            LOG.debug('REQUEST: GET %s', req)
            r = requests.get(req, auth=rest_client.auth)
            r.raise_for_status()
            return r.json()
        return get_decorator

def query(name, value=None):
    """
    Query parameter decorator
    """
    def query_decorator(f):
        if not hasattr(f, '_query__parameters'):
            f._query__parameters = {}
        f._query__parameters[name] = value
        return f
    return query_decorator

def body(name, value=None):
    """
    Body parameter decorator
    """
    def body_decorator(f):
        f._body__parameter = value
        return f
    return body_decorator


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



