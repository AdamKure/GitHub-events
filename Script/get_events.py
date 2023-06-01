
# import sseclient
import requests
from datetime import datetime, timedelta


class GitHubEvents:

    def __init__(self, desired_events: list, offset_minutes: int=10, **kwargs):  # upravit kwargs
        self.events = []
        self.count_events = []
        self.url = "https://api.github.com/events"
        self.desired_events = desired_events
        self.offset_minutes = offset_minutes
        
        # # room for other arguments for repos, users ets
        # self.user_name = kwargs.get("user_name")
        # self.repo_name = kwargs.get("repo_name")
        # if self.user_name and self.repo_name:
        #     self.url +=  f"{self.user_name}/{self.repo_name}"

    def get_event_count(self):
        self.__update_events()
        offset_data = self.__filter_by_offset()
        event_count = {}
        for event_type in self.desired_events:
            event_count[event_type] = 0

        for event in offset_data:
            event_count[event["event_type"]] += 1

        return event_count

    def get_avg_time_pull(self, repo_id: int):
        self.__update_events()
        pull_event_list = [event for event in self.events if event["event_type"]=="PullRequestEvent" and event["repo_id"] == repo_id]
        if len(pull_event_list) < 2:
            raise ValueError("Less than 2 entries")
        
        sorted_pull_list = sorted(pull_event_list, key=lambda x: x["event_time"])  # time increases with increasing index

        first_entry_time = datetime.strptime(sorted_pull_list[0]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
        last_event_time = datetime.strptime(sorted_pull_list[-1]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
        total_time_diff = last_event_time - first_entry_time
        number_of_diffs = len(sorted_pull_list) - 1
        avg_time_diff = total_time_diff / number_of_diffs
        return avg_time_diff

    def __update_events(self):
        page = 1
        
        while(True):
            update_date = self.__fetch_events()
            try:
                self.__add_events(update_date)
            except ValueError():
                break
            page += 1  # bacha aby se pri updatu neposunuly data z p1 na p2

    def __filter_by_offset(self):
        desired_time = datetime.now() - timedelta(minutes=self.offset_minutes)
        sorted_events = sorted(self.events, key=lambda x: x["event_time"])
        offset_events = []
        for event in sorted_events:
            if datetime.strptime(event["event_time"], "%Y-%m-%dT%H:%M:%SZ") >= desired_time:
                offset_events.append(event)
            else:
                break

        return offset_events

    def __fetch_events(self, page: int=1, events_per_page: int=2):
        payload = {
            "accept": "application/json",
            "per_page": events_per_page,
            "page": page
        }

        response = requests.get(self.url, params=payload, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 304:
            return
        else:
            raise requests.exceptions.HTTPError(f"Unexpected response: {response.status_code}")
        # sse client here maybe

    def __add_events(self, added_data: list):
        for event in added_data:
            event_type = event["type"]
            if event_type not in self.desired_events:
                continue
            
            event_id = event["id"]
            if event_id in self.events:
                raise ValueError("Id already in event list")

            event_time = event["created_at"]
            repo_id = event["repo"]["id"]

            self.events.append({
                "event_id": event_id,
                "event_type": event_type,
                "event_time": event_time,
                "repo_id": repo_id        
            })

if __name__ == "__main__":
    wanted_events = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']
    mc = GitHubEvents(wanted_events)
    print(mc.url)
    print(mc.get_event_count())
    print(mc.get_avg_time_pull("2045"))

    # chybi stale dodelat pocet itemu a automaticky refresh
