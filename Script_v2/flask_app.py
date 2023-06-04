import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_get_request():
    for header, value in request.headers.items():
        pass

    if request.get_data():
        try:
            body_params = json.loads(request.get_data())
            for param, value in body_params.items():
                print(f"{param}: {value}")
        except json.JSONDecodeError:
            print("Invalid JSON in the request body")

    return "Success"

if __name__ == "__main__":
    app.run()
