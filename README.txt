This repo contains a module that runs a simple flask server acting as an API through which you can get certain Event data from https://www.github.com.
    - Get number of IssuesEvents, PullRequestEvents and WatchEvents in the last n minutes
    - Get average time between PullRequests for a specific repository
    - Sends back donut chart visualizing the ration of each event type in last few minutes

Dependencies:
    - flask
    - io
    - json
    - re
    - requests
    - secret.py: python file that stores the GitHub authorization token

Global Variables:
    - TOKEN: Authorization token for GitHUb. Stored in secret.py in main directory

Classes:
    - EventHandler: Stores events data and is able to perfom certain analytical operations on it.
    - GitHubFetcher: Stores methods for fetching items from GitHub's API.
    - Flask: Flask server

Please make sure that you have a secret.py containing your authorization token to GitHub before runnig the server.
Example file secret.py is included.

The C4 level 1 diagram is included as c4-1.png.

To do: 
    - Add fetching functionality (user, organizations, repository networks)
    - Add visualizing methods
    - implement webhooks
    - Implement caching
    - Add tests (unit, imtegration, ...) 

Author: AdamKure