from events_fetcher import GitHubFetcher

class EventHolder:
    def __init__(self, cached_events: dict=None):
        if cached_events:
            self.cached_events = cached_events
        else:    
            self.cached_events = {}  # event id keys with event data as a value

        self.lookup_ids = {}  # lookup dict with keys of cached_events for fast search 
        for key in self.cached_events.keys():
            self.lookup_ids[key]: ""
    
    def get_events_repo(self, owner, repo, force_update=False):
        if force_update:
            self.update_events_repo(owner, repo)
        repo_events = {}
        for event in self.cached_events.values():
            repo_id = event["repo"]["id"]  # dodelat

    def update_events_offset(self, offset: int):
        ghf = GitHubFetcher()
        fetched_data = ghf.fetch_by_offset(offset)
        filtered_data = self.select_event_types(fetched_data)  # dodelat
        for event in filtered_data:
            event_id = event["id"]
            if self.is_cached(event_id):
                continue
            else:
                self.cached_events[event_id]: event
                self.lookup_ids[event_id]: ""

    def update_events_repo(self, owner: str, repo: str):
        ghf = GitHubFetcher()
        fetched_data = ghf.fetch_from_repo(owner, repo)
        filtered_data = self.select_event_types(fetched_data) ## odelat
        for event in filtered_data:
            event_id = event["id"]
            if self.is_cached(event_id):
                continue
            else:
                self.cached_events[event_id]: event
                self.lookup_ids[event_id]: ""

    def is_cached(self, event_id: str):     
        if event_id in self.lookup_ids:
            return True
        else:
            return False

    def select_event_types(self, unfiltered_events: list, desired_events: list):
        filtered_events = []
        for event in unfiltered_events:
            event_type = event["type"]
            if event_type in desired_events:
                filtered_events.append: event
        return filtered_events




pull_evemt = ['PullRequestEvent']
wanted_events = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']
example_type = {"id": {"dict_with_other_info": ""}}