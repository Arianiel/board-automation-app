# app.py

from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.json)
        # print(request.json["action"])
        match request.json["action"]:
            case "unlabeled":
                print("Label removed: ", request.json["label"]["name"])
            case "labeled":
                print("Label added: ", request.json["label"]["name"])
            case _:
                print("No cases for action: ", request.json["action"])
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run()