from flask import Flask, escape, request
from flask import jsonify, render_template
import config
from time import sleep

__version__ = "0.1"

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get("name", "World")
    return render_template("index.html")


@app.route('/api/v1/send', methods=["POST"])
def send():
    # bot.send_message("test")
    print(request.headers)
    content = request.json

    message = content.get("message")
    if message:
        return jsonify({"state": "success"})
    else:
        return jsonify({"state": "error", "info": "message is empty"}), 400

@app.route('/api/v1/record')
def record():
    print("record started")
    sleep(5)
    return jsonify({"state": "success", "info": "record finished"})


# test client
# client = requests.post("http://127.0.0.1:5000/api/v1/send", json={"message":"hello"}, auth=HTTPBasicAuth(<token_string>,""))
