

class QueryBuilder(object):

    def __init__(self, config):
        self.config = config

    def project_endpoint(self, project_id=None):
        if project_id == None or project_id == "":
            return self.config.get_endpoint('jira') + "/project"
        else:
            return self.config.get_endpoint('jira') + "/project/%s" % (project_id)
