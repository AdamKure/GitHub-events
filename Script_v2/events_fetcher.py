import requests
from datetime import datetime, timedelta
import re

class GitHubFetcher:
    def __init__(self, cached_ids: dict=None):
        if cached_ids is None:
            self.cached_ids = {}
        else:
            self.cached_ids = cached_ids
        # prozatim priprava na cachovani

    def fetch_from_repo(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/events"
        headers = {
            "accept": "application/json",
            "per_page": 3,
        }
        response = requests.get(url, headers=headers, timeout=3)
        
        
        # uplne to oddelit do paginator metody
        all_data = []
        while(True):  # loop to get all the pages, maybe page limit as a condition
            if response.status_code == 304:
                break
            elif response.status_code != 200:
                raise requests.exceptions.HTTPError(f"Unexpected response: {response.status_code}")

            page_data = response.json()
            all_data += page_data
            # podminka zda posledni ziskane id uz je v eventech a pokud ne tak dalsi stranku
            if page_data[-1]["id"] in self.cached_ids:
                break
            
            url = self.get_next_page_url(response)
            if not url:
                break

            response = requests.get(url, timeout=3)
      
        return all_data
  
    def fetch_by_offset(self, offset):
        desired_time = datetime.now() - timedelta(minutes=offset)
        url = "https://api.github.com/events"
        headers = {
            "accept": "application/json",
            "per_page": 3,
        }

        response = requests.get(url, headers=headers, timeout=3)
        
        all_data = []
        while(True):  # loop to get all the pages, maybe page limit as a condition
            if response.status_code == 304:
                break
            elif response.status_code != 200:
                raise requests.exceptions.HTTPError(f"Unexpected response: {response.status_code}")

            page_data = response.json()
            all_data += page_data

            last_event_time = datetime.strptime(page_data[-1]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if last_event_time < desired_time:
                break
            
            url = self.get_next_page_url(response)
            if not url:
                break

            response = requests.get(url, timeout=3)

        return all_data

    def get_next_page_url(self, response):
        link_header = response.headers["link"]
        link_pattern = r'<(.*?)>; rel="next"'
        match = re.search(link_pattern, link_header)
        
        if match:
            url = match.group(1)
            return url
        else:
            return
 

if __name__ == "__main__":
    mc = GitHubFetcher()
    data = mc.fetch_from_repo("yanyongyu", "githubkit")
    # print(data)
    # with open("C:\Users\Adam\Documents\Python Scripts\Datamole\Script_v2\events.json", 'a') as file:
    #     for event in data:
    #         file.write(json.dump(event))
