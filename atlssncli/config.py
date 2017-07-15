import ConfigParser
import logging as LOG
from os.path import expanduser, join
from sets import Set
import logging

HOME_DIR = expanduser("~")
CONFIG_DIR = join(HOME_DIR, ".atlssncli")
CONFIG_PATH = join(CONFIG_DIR, "config.ini")
CACHE_DIR = join(CONFIG_DIR, "cache")

# Cached list of projects for autocompletion
PROJECTS_CACHE = join(CACHE_DIR, "_projects")

# Cached list of issues for autocompletion
ISSUES_CACHE = join(CACHE_DIR, "_issues")

# Cached list of issue types for autocompletion
ISSUETYPES_CACHE = join(CACHE_DIR, "_issuetypes")

# Cached list of build plans for autocompletion
PLANS_CACHE = join(CACHE_DIR, "_plans")

# Cached list of users for autocompletion
USERS_CACHE = join(CACHE_DIR, "_users")

# Required config sections
REQUIRED_SECTIONS = Set(['common', 'jira', 'bitbucket', 'bamboo'])


class Config(object):

    def __init__(self, config_path = CONFIG_PATH):
        self.path = config_path
        self.config = ConfigParser.ConfigParser()
        LOG.debug('Reading configuration from %s', self.path)
        self.config.read(self.path)
        LOG.debug('Got configuration sections: %s', 
                ",".join(self.config.sections()))

    def validate(self):
        """Validate the config file"""
        if not REQUIRED_SECTIONS.issubset(Set(self.config.sections())):
            raise Exception("Missing required config sections: %s"%
                      (",".join(REQUIRED_SECTIONS.
                          difference(Set(self.config.sections())))))
        return True

    def get_auth(self, service = None):
        """Return the authentication credentials for service"""
        return (self.config.get('common', 'username'), 
                self.config.get('common', 'password'))

    def get_endpoint(self, service):
        """Get endpoint of specific service"""
        return self.config.get(service, 'endpoint')

