# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    WebhookParser,
    LineBotApi
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from action import ActionManager

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

parser = WebhookParser(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    

    # parse webhook body
    try:
        events = parser.parse(body, signature)
        app.logger.info("Events: " + str(events))
    except InvalidSignatureError:
        abort(400)

    api_client = ApiClient(configuration)
    #line_bot_api = MessagingApi(api_client)
    line_bot_api = LineBotApi(channel_access_token)
    act_mgr = ActionManager(line_bot_api)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        event_json = event.as_json_dict()
        if event_json['type'] == 'postback':
            if event_json['postback']['data'] == 'send_postback':
                user_id = event_json['source']['userId']
                #app.logger.info("User ID: " + user_id)
                act_mgr.onboard_date(user_id)
            #elif event_json['postback']['data'] == 'datetime_postback':
                
        #app.logger.info("Event: " + str(event_json))
        #if not isinstance(event, MessageEvent):
        #    app.logger.info("Not MessageEvent")
        #    continue
        #if not isinstance(event.message, TextMessageContent):
        #    app.logger.info("Not TextMessageContent")
        #    continue
        #line_bot_api = MessagingApi(api_client)
        #user_profile = line_bot_api.get_profile(event_json['source']['userId'])
        #app.logger.info("Users: " + str(user_profile.display_name))
       
        #with ApiClient(configuration) as api_client:
       #     line_bot_api = MessagingApi(api_client)
            #print('Event': )
       #     user_profile = line_bot_api.get_profile(event['source']['userId'])
       #     app.logger.info("User Profile: " + str(user_profile))
            #line_bot_api.reply_message_with_http_info(
            #    ReplyMessageRequest(
            #        reply_token=event.reply_token,
            #        messages=[TextMessage(text=event.message.text)]
            #    )
            #)

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
