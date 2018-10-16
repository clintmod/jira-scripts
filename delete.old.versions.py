import json
import os
import requests
from requests.auth import HTTPBasicAuth

username = os.environ['JIRA_USERNAME']
password = os.environ['JIRA_PASSWORD']

auth = HTTPBasicAuth(username,password)
result = requests.get ('https://jira.verticalresponse.com/rest/api/2/project/VR2/versions', auth=auth ) 

releases = json.loads(result.text)
releases = sorted(releases, key=lambda rel: ':'.split(rel['name'])[0].strip())
bad_releases = []
for release in releases:
  if not release['name'].startswith('r'):
    bad_releases.append(release)
print json.dumps(bad_releases, sort_keys=True, indent=4, separators=(',', ': '))

for bad_release in bad_releases:
  rel = bad_release['id']
  uri = "https://jira.verticalresponse.com/rest/api/2/version/" + bad_release['id']
  print "uri = " + uri
  response = requests.delete(uri, auth=auth)

