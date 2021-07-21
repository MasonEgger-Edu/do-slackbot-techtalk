import os
import random
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))

slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "",
    },
}

@slack_events_adapter.on("message")
def message(payload):
    
    event = payload.get("event", {})

    text = event.get("text")

    if "flip a coin" in text.lower():
        channel_id = event.get("channel")

        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        message = f"The result is {results}"

        MESSAGE_BLOCK["text"]["text"] = message

        x = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}

        return slack_web_client.chat_postMessage(**x)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)