from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the payload from the request
    payload = request.get_json()

    # Define the event types you want to listen to
    event_types = ['IssuesEvent', 'PullRequestEvent', 'WatchEvent']

    # Filter the events based on the desired event types
    filtered_events = [event for event in payload if event['type'] in event_types]

    # Save the filtered events to a local JSON file
    file_path = "/events.json"
    with open(file_path, 'a') as file:
        for event in filtered_events:
            file.write(json.dumps(event) + '\n')

    return 'Webhook received'

if __name__ == '__main__':
    app.run()
