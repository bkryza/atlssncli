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
# limitations under the License.

import configparser
import logging as LOG
from os.path import expanduser, join

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
REQUIRED_SECTIONS = set(['common', 'jira', 'bitbucket', 'bamboo'])


class Config(object):

    def __init__(self, config_path=CONFIG_PATH):
        self.path = config_path
        self.config = configparser.ConfigParser()
        LOG.debug('Reading configuration from %s', self.path)
        self.config.read(self.path)
        LOG.debug('Got configuration sections: %s',
                  ",".join(self.config.sections()))

    def validate(self):
        """Validate the config file"""

        if not REQUIRED_SECTIONS.issubset(set(self.config.sections())):
            raise Exception("Missing required config sections: %s" %
                            (",".join(REQUIRED_SECTIONS.
                                      difference(set(self.config.sections())))))
        return True

    def get_auth(self, service=None):
        """Return the authentication credentials for service"""

        return (self.config.get('common', 'username'),
                self.config.get('common', 'password'))

    def get_endpoint(self, service):
        """Get endpoint of specific service"""

        return self.config.get(service, 'endpoint')

    def get_board(self):
        """Get active board"""

        return self.config.get('agile', 'board')

    def set_board(self, board_id):
        """Set default board"""

        self.config.set('agile', 'board', board_id)
        self.sync()

    def get_sprint_duration(self):
        """Get active board"""

        return self.config.get('agile', 'sprint_duration')

    def get_project(self):
        """Get active project"""

        active_project = self.config.get('common', 'active_project')

        return active_project

    def set_project(self, project):
        """Set active project"""

        self.config.set('common', 'active_project', project)
        self.sync()

    def get_repo_plan_ids(self, repo):
        """Get Bamboo plan ids related to a repository by repository name"""

        return tuple(self.config.get('bamboo', repo).split(','))

    def sync(self):
        """Update configuration file"""
        LOG.debug("SYNC, sections: %s", self.config.sections())

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
