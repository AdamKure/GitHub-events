"""
This module runs a flask server acting as an API through which you can get certain Event data from GitHub.
    - Get number of IssuesEvents, PullRequestEvents and WatchEvents in the last n minutes
    - Get average time between PullRequests for a specific repository
    - Sends back donut chart visualizing the ration of each event type in last few minutes

Dependencies:
    - flask
    - io
    - json
    - re
    - requests
    - secret.py: python file in main directory that stores the GitHub authorization token

Global Variables:
    - TOKEN: Authorization token for GitHUb. Stored in secret.py

Classes:
    - EventHandler: Stores events data and is able to perfom certain analytical operations on it.
    - GitHubFetcher: Stores methods for fetching items from GitHub's API.
    - Flask: Flask server
"""

from GHEvents import server


HOST = "localhost"
PORT = 5000

server.app.run(host=HOST, port=PORT)
