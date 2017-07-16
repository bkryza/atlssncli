

class CommandGroup(object):
    def __init__(self, config):
        self.config = config
        pass
    def get_config(self):
        return self.config

class Project(CommandGroup):
    def __init__(self, config):
        super(Project, self).__init__(config)

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

class Docs(CommandGroup):
    def __init__(self, config):
        super(Docs, self).__init__(config)


