from atlssncli.rest import jiraclient
from requests.auth import HTTPBasicAuth
import json

c = jiraclient.JiraClient('https://jira.onedata.org/rest/api/latest')
c._set_auth(HTTPBasicAuth('plgkryza', 'KAVg6NH5ax_WC'))

res = c.get_all_projects()

projects = []

for project in res:
    projects.append([project['key'], project['id'], project['name']])

print(str(projects))
