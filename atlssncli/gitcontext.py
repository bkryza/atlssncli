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

import re

from pygit2 import Repository

issue_id_regexp = re.compile(r'.*/(.*-\d+)-.*')

def get_branch():
    """ """
    branch = Repository('.').head.shorthand
    return branch

def get_repo_name():
    """ """
    repo_url = Repository('.').remotes['origin'].url
    return repo_url.split('/')[-1]

def get_issue_id():
    """ """
    branch = Repository('.').head.shorthand
    res = re.search(issue_id_regexp, branch)
    if res.group(1):
        return res.group(1)
    else:
        return ''

