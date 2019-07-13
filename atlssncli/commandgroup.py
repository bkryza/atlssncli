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

class CommandGroup(object):
    def __init__(self, config):
        self.config = config
        pass

    def get_config(self):
        return self.config


class Agent(CommandGroup):
    def __init__(self, config):
        super(Agent, self).__init__(config)


class Project(CommandGroup):
    def __init__(self, config):
        super(Project, self).__init__(config)


class Board(CommandGroup):
    def __init__(self, config):
        super(Board, self).__init__(config)


class Issue(CommandGroup):
    def __init__(self, config):
        super(Issue, self).__init__(config)


class Git(CommandGroup):
    def __init__(self, config):
        super(Git, self).__init__(config)


class Build(CommandGroup):
    def __init__(self, config):
        super(Build, self).__init__(config)


class Agile(CommandGroup):
    def __init__(self, config):
        super(Agile, self).__init__(config)


class Sprint(CommandGroup):
    def __init__(self, config):
        super(Sprint, self).__init__(config)


class Docs(CommandGroup):
    def __init__(self, config):
        super(Docs, self).__init__(config)


class Info(CommandGroup):
    def __init__(self, config):
        super(Info, self).__init__(config)
