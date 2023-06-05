""" This module contains GitHubFetcher object containing methods for fetching data from github """

import json
import re
import requests
from datetime import datetime, timedelta
from secret import TOKEN


class GitHubFetcher:
    """
    Stores methods for fetching items from GitHub's API.
    Can fetch event from github limited by time through .fetch_by_offset
    Can fetch event from github specific repository through .fetch_from_repo
    
    Relies on "requests", "datetime" and "re" modules.
    Current version methods obtain all the data, caching is not implemented.
    """

    # def __init__(self, cached_events: dict=None):
    #     if cached_events is None:
    #         self.cached_events = {}
    #     else:
    #         self.cached_events = cached_events

    def fetch_from_repo(self, owner: str=None, repo_name: str=None, repo_id: int=None):
        """
        Method used for fetching items from a specific repo.
        Please make sure you have personal access token in config.py

        Repo can be described by either passing "owner" and "repo_name", or by passing "repo_id",
        if all are provided, "repo_id" is used
        (Both arguments are part of repo URL as https://github.com/owner/repo)

        :param owner: Username of repository's owner
        :param repo_name: Name of the repository
        :param repo_id: Id of the repo
        :return: Returns list of dictionaries each containing a single event data

        Examples:
        --------
        .fetch_from_repo(repo_id=1234567)
        or
        .fetch_from_repo("octokit", "octokit.js")
        """

        if repo_id:
            url = f"https://api.github.com/repositories/{repo_id}/events"
        elif owner and repo_name:
            url = f"https://api.github.com/repos/{owner}/{repo_name}/events"
        else:
            raise ValueError("Either REPO_ID or both OWNER and REPO_NAME have to be passed")

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "accept": "application/json"
        }
        payload = {"per_page": 100}
        response = requests.get(url, headers=headers, params=payload, timeout=3)

        # loop to get all the pages, page limit through a condition could be implemented as well
        all_data = []
        while True:
            if response.status_code != 200:
                raise requests.exceptions.HTTPError(f"Unexpected response: {response.status_code}")

            page_data = response.json()
            all_data += page_data

            url = self.__get_next_page_url(response)
            if not url:
                break

            response = requests.get(url, headers=headers, timeout=3)

        return all_data

    def fetch_by_offset(self, offset: int):
        """
        Method used for fetching items from the whole GitHUb limited by time offset.

        :param offset: Specifies the offset length in minutes
        :return: Returns list of dictionaries containing event data (JSON format)
        """

        url = "https://api.github.com/events"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "accept": "application/json"
        }
        payload = {"per_page": 100}
        response = requests.get(url, headers=headers, params=payload, timeout=3)

        desired_time = datetime.utcnow() - timedelta(minutes=offset)
        all_data = []
        while True:  # loop to get all the pages, page limit through a condition could be implemented as well
            if response.status_code != 200:
                raise requests.exceptions.HTTPError(f"Unexpected response: {response.status_code}")

            page_data = response.json()
            all_data += page_data

            last_event_time = datetime.strptime(page_data[-1]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            # stop fetching when fetched data are older than desired time
            if last_event_time < desired_time:
                break

            url = self.__get_next_page_url(response)
            if not url:
                break

            response = requests.get(url, headers=headers, timeout=3)

        return all_data

    def __get_next_page_url(self, response: "requests.Response object"):
        """
        Extracts next page url from the response object

        :param response: Response object obtained as a response from request.get()
        :return: URL (string) for the next page or "None" if the response does not contain it
        """

        link_header = response.headers["link"]
        link_pattern = r'<(.*?)>; rel="next"'
        match = re.search(link_pattern, link_header)

        if match:
            url = match.group(1)
            return url
        else:
            return

    # def update_cached_events(self, cached_events: dict):
    #     self.cached_events = cached_events


if __name__ == "__main__":
    # fetches data and saves it as json flles
    mc = GitHubFetcher()
    data_1 = mc.fetch_by_offset(6)
    data_2 = mc.fetch_from_repo("yanyongyu", "githubkit")

    with open('offset.json', 'w') as file:
        json.dump(data_1, file)

    with open('repo.json', 'w') as file:
        json.dump(data_2, file)

    # display number of fetched items
    print(f"offset fetched {len(data_1)} items")
    print(f"repo fetched {len(data_2)} items")

    print("""
    "You can check the desired data format at:"
    "https://docs.github.com/en/rest/activity/events"
    """)
