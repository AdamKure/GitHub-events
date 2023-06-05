""" Contains basic HTTP server with basic API settings for getting GitHub events stats """
import flask
from event_handler import EventHandler

HOST = "localhost"
PORT = 5000

app = flask.Flask(__name__)
handler = EventHandler()

@app.route("/")
def main_page_greet():
    """
    Displays simple greetings on main page with information how to send requests
    Requires main_page.html
    """

    with open("main_page.html", "r") as file:
        body = file.read()
    return body

@app.route("/api/pull-time", methods=['GET'])
def handle_pull_time():
    """ Settings for handling API request on PullEvents times """

    if flask.request.method == 'GET':
        payload = flask.request.args.to_dict()

        owner = payload.get('owner')
        repo_name = payload.get('repo_name')
        repo_id = payload.get("repo_id")
        if not repo_id and not(owner and repo_name):
            return flask.make_response("Bad Request", 400)

        if repo_id:
            repo_id = int(repo_id)

        try:
            time_data = handler.get_repo_pull_time(owner, repo_name, repo_id)
        except Exception:  # if enough time should implement each exception differently
            return flask.make_response("Not Found", 404)
        else:
            response = {"avg_duration": str(time_data)}
            return flask.jsonify(response)


@app.route("/api/global-event-stats", methods=['GET'])
def handle_global_event_stats():
    """ Settings for handling API request on events stats """

    if flask.request.method == 'GET':
        payload = flask.request.args.to_dict()

        offset = payload.get('offset')
        if not offset:
            return flask.make_response("Bad Request", 400)
        else:
            offset = int(offset)
            print(offset)

        try:
            data = handler.get_events_count_offset(offset)
        except Exception:  # if enough time should implement each exception differently
            return flask.make_response("Not Found", 404)
        else:
            return flask.jsonify(data)

@app.route("/api/visualize", methods=['GET'])
def handle_visualize():
    """ Settings for handling API request to visualizations """

    pass
    # if flask.request.method == 'GET':
    #     payload = flask.request.args.to_dict()

    #     offset = payload.get('offset')
    #     if not offset:
    #         return flask.make_response("Bad Request", 400)
    #     else:
    #         offset = int(offset)
    #         print(offset)

    #     try:
    #         data = handler.get_events_count_offset(offset)
    #     except Exception:  # if enough time should implement each exception differently
    #         return flask.make_response("Not Found", 404)
    #     else:
    #         return flask.jsonify(data)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
