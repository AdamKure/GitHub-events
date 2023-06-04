from events_fetcher import GitHubFetcher
from datetime import datetime, timedelta

class EventHolder:
    """
    Stores events data and is able to perfom certain analytical operations on it.
    
    Calls GitHubFetcher when it needs to fetch data from GitHub.

    No caching functionality yet.
    """
    def __init__(self):
        # self.cached_events = {}
        # self.cached_repos = {}
        self.fetcher = GitHubFetcher()

    def get_repo_pull_time(self, owner: str=None, repo_name: str=None, repo_id: int=None):
        """
        Calculates mean time between 2 pull requests in a specific repository.

        :param owner: Username of repo's owner
        :param repo_name: Name of the repository
        :param repo_id: Repository id
        :return: Mean time for a pull request; datetime object
        """
        # hardset event types I want
        desired_types = ['PullRequestEvent']

        fetched_data = self.fetcher.fetch_from_repo(owner, repo_name, repo_id)
        filtered_data = self.filter_event_types(fetched_data, desired_types)

        if len(filtered_data) < 2:
            raise ValueError("Less than 2 entries")

        sorted_data = sorted(filtered_data, key=lambda x: x["created_at"], reverse=True)

        # instead of averaging all the diffs I can use total time diffs and number of diffs
        last_event_time = datetime.strptime(sorted_data[0]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
        first_entry_time = datetime.strptime(sorted_data[-1]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
        total_time_diff = last_event_time - first_entry_time
        number_of_diffs = len(sorted_data) - 1
        avg_time_diff = total_time_diff / number_of_diffs
        return avg_time_diff

    def get_events_count_offset(self, offset: int):
        """
        Calculates number of each specified event type created in last n minutes

        :param offset: Specifies the number of minutes

        :return: Dict of event types (keys) and number of events (values)
        """
        desired_types = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']
        desired_time = datetime.now() - timedelta(minutes=offset)

        fetched_data = self.fetcher.fetch_by_offset(offset)
        filtered_types = self.filter_event_types(fetched_data, desired_types)
        filtered_data = self.filter_offset(filtered_types, desired_time)

        event_count = {event_type: 0 for event_type in desired_types}
        for event in filtered_data:
            event_count[event["type"]] += 1
        return event_count


    def filter_event_types(self, unfiltered_events: list, desired_types: list):
        """
        Keeps only events with event types that are specified in "desired_types"

        :param unfiltered_events: Events that are going to be filtered
        :param desired_types: Event types that shall be kept, others will be removed

        :return: List of events specified in "desired_events"
        """
        filtered_events = [event for event in unfiltered_events if event["type"] in desired_types]
        return filtered_events

    def filter_offset(self, unfiltered_events: list, desired_time: "datetime object"):
        """
        Filters events that were created after specified datetime

        :param unfiltered_events: Events that are going to be filtered
        :param desired_time: Events older than this datetime will be removed

        :return: List of events younger than desired_time
        """

        filtered_events = [event for event in unfiltered_events if self.get_event_time(event) >= desired_time]
        return filtered_events

    def get_event_time(self, event: dict):
        """
        Returns GitHub event creation time as datetime object
        in format YYYY-MM-DD HH:MM:SS.Z
        """
        return datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    # def is_cached_event(self, event_id: str):
    #     if event_id in self.cached_events:
    #         return True
    #     else:
    #         return False

    # def is_cached_repo(self, owner: str= None, repo_name: str=None, repo_id: int=None):
    #     if (owner, repo_name) in self.cached_repos.keys() or repo_id in self.cached_repos.values():
    #         return True
    #     else:
    #         return False



# Example:
# cached_events = {"idstring": "subdictionary"}
# cached_repos = {("owner", "repo_name"): "repoid"}
# pull_evemt = ['PullRequestEvent']
# wanted_events = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']
# example_type = {"id": {"dict_with_other_info": ""}}

if __name__=="__main__":
    print()
