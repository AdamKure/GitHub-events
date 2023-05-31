import requests
import time
# import json
# import sseclient

GLOBAL_GITHUB = True  # specifies if the whole github should be searched or just part



url = "https://api.github.com/events"
repo_appendix = "user_name/repo_name"

if not GLOBAL_GITHUB:
    url += repo_appendix

wanted_events = ('WatchEvent', 'PullRequestEvent', 'IssuesEvent')

payload = {
    "accept": "application/vnd.github+json",
    "per_page": 2,
    'events': ','.join(events)
}

response = requests.get(url, params=payload)
data = response.json()


# client = sseclient.SSEClient(request)

print(response.status_code)

offset = 3
events = {}
for wanted_event in wanted_events:
    events[event] = []


for event in data:
    event_type = event["type"]
    event_id = event["id"]
    repo_id = ["repo"]["id"]
    event_time = event["created_at"]

print(data[0])
