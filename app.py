import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

import json

import requests

load_dotenv()


machine = TocMachine(
    states=["user", "todayweather", "city", "picture", "air", "weekweather", "weekcity", "graph", "state"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state",
            "conditions": "is_going_to_state",
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "todayweather",
            "conditions": "is_going_to_todayweather",
        },
        {
            "trigger": "advance",
            "source": "todayweather",
            "dest": "city",
            "conditions": "is_going_to_city",
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "air",
            "conditions": "is_going_to_air",
        },
        {
            "trigger": "advance",
            "source": "state",
            "dest": "weekweather",
            "conditions": "is_going_to_weekweather",
        },
        {
            "trigger": "advance",
            "source": "weekweather",
            "dest": "weekcity",
            "conditions": "is_going_to_weekcity",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "graph",
            "conditions": "is_going_to_graph",
        },
        {"trigger": "go_back", "source": ["todayweather", "city", "picture", "air", "weekweather","weekcity", "graph"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "請輸入hi或graph")
            machine.go_back()

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    try:
        machine.get_graph().draw("fsm.png", prog="dot", format="png")
        return send_file("fsm.png", mimetype="image/png")
    except Exception as ex:
        # sys.exc_info()[0] 就是用來取出except的錯誤訊息的方法
        print(ex)

@app.route("/show-week", methods=["GET"])
def show_week():
    # city = "嘉義市"
    # city = request.args.get('city')
    # print(city)
    return send_file("week.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)