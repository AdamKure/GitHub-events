import requests


def test_repo_pull():
    params = {"owner": "octokit", "repo_name": "request-action", "repo_id": ""}
    response1 = requests.get("http://localhost:5000/api/pull-time", params=params, timeout=5)
    print(response1.status_code)
    if response1.status_code == 200:
        print(response1.json())


def test_offset():
    response2 = requests.get("http://localhost:5000/api/global-event-stats", params={"offset": 6}, timeout=5)
    print(response2.status_code)
    if response2.status_code == 200:
        print(response2.json())


if __name__ == "__main__":
    test_repo_pull()
    # test_offset()
