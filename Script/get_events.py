
# import sseclient
import requests
from datetime import datetime, timedelta


class GitHubEvents:

    def __init__(self, desired_events):
        self.desired_events = desired_events
        self.url = "https://api.github.com/events"
        self.url_appendix = "user_name/repo_name"
        if not GLOBAL_GITHUB:
            self.url += self.url_appendix
        self.events = []
        self.count_events = []
    
    def update_events(self):
        update_date = self._fetch_events()
        self._add_events(update_date)

    def get_event_count(self):
        event_count = {}
        for event_type in self.desired_events:
            event_count[event_type] = 0

        for event in self.events:
            event_count[event["event_type"]] += 1

        return event_count

    def get_avg_time_pull(self):
        pull_event_list = (event for event in self.events if event["event_type"]=="PullRequestEvent")
        if len(pull_event_list) < 2:
            raise ValueError("Less than 2 entries")
        
        sorted_pull_list = sorted(pull_event_list, key="event_time")

        total_time_diff = sorted_pull_list[0] - sorted_pull_list[-1]
        number_of_diffs = len(sorted_pull_list) - 1
        return total_time_diff / number_of_diffs

    def filter_by_offset(self, offset_minutes=10):
        desired_time = datetime.now() - timedelta(minutes=offset_minutes)
        sorted_events = sorted(self.events, key="event_time")
        offset_events = []
        for event in sorted_events:
            if event["event_time"] >= desired_time:
                offset_events.append(event)
            else:
                break

        return offset_events

    def _fetch_events(self):
        payload = {
            "accept": "application/json",
            "per_page": COUNT
        }

        response = requests.get(self.url, params=payload, timeout=3)
        print(response.status_code)  # handle 304 potřeba dodelat
        #sem neco kdyz 304
        data = response.json()
        return data
        #sse client here maybe

    def _add_events(self, added_data: list[dict]):
        for event in added_data:
            event_type = event["type"]
            if event_type not in self.desired_events:
                continue
            
            event_id = event["id"]
            if event_id in self.events:
                continue

            event_time = event["created_at"]
            repo_id = event["repo"]["id"]

            # swich pres dict na rozdeleni do 
            self.events.insert({
                "event_id": event_id,
                "event_type": event_type,
                "event_time": event_time,
                "repo_id": repo_id        
            })  # mozna list.insert pro novy   


if __name__ == "__main__":
    GLOBAL_GITHUB = True  # specifies if the whole github should be searched or just part
    COUNT = 10
    wanted_events = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']
    mc = GitHubEvents(wanted_events)
    print(mc._fetch_events())
    print(mc.get_event_count())
    print(mc.get_event_count())
