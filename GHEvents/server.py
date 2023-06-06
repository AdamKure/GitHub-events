""" Contains basic HTTP server with basic API settings for getting GitHub events stats """
import flask
from GHEvents.event_handler import EventHandler
from io import BytesIO


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
            return flask.make_response("Internal Server Error", 500)
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

        if offset <= 5:
            return flask.make_response("Bad Request", 400)

        try:
            data = handler.get_events_count_offset(offset)
        except Exception:  # if enough time should implement each exception differently
            return flask.make_response("Internal Server Error", 500)
        else:
            return flask.jsonify(data)

@app.route("/api/visualize", methods=['GET'])
def handle_visualize():
    """ Settings for handling API request to visualizations """

    if flask.request.method == 'GET':
        payload = flask.request.args.to_dict()

        # other params for other methods can be added later
        update = payload.get("update", False)
        type_ratio = payload.get("type_ratio", False)

        if not type_ratio:
            return flask.make_response("Bad Request", 400)

        # in future separate method to update data can be implemented, now i use get_events_count_offset
        if update:
            try:
                handler.get_events_count_offset(6)
            except Exception:  # if enough time should implement each exception differently
                return flask.make_response("Internal Server Error", 500)

        try:
            handler.visualize_event_type_ratio()
        except Exception:  # if enough time should implement each exception differently
            return flask.make_response("Internal Server Error", 500)
        else:
            with open("chart.png", 'rb') as file:
                img = file.read()
            return flask.send_file(BytesIO(img), mimetype='image/png', as_attachment=True, download_name="chart.png")


if __name__ == "__main__":
    app.run(debug=True)
