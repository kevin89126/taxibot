import os
from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫
#from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate, ConfirmTemplate
from linebot.models import MessageAction, TemplateSendMessage, ConfirmTemplate
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TemplateMessage
)


from action import ActionManager

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

configuration = Configuration(
    access_token=channel_access_token
)

with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
#line_bot_api = LineBotApi('ysfHtOOPjknbC3sRMjrZdMJ0aoLxLYSw/e6KL7UGvmulYW+H7I9wcnFZbr1X1C9T+heH8me/kwRpsXO+wWa4giQ+D/7j7MqtwBwdYWvkCLHqdcDVyfnpeken3pk5MAR59MBtz7e23tc9gi96DCb4kQdB04t89/1O/w1cDnyilFU')
            buttons_template = ButtonsTemplate(
                title='My buttons sample',
                text='Hello, my buttons',
                actions=[
                    URIAction(label='Go to line.me', uri='https://line.me'),
                    PostbackAction(label='ping', data='ping'),
                    PostbackAction(label='ping with text', data='ping', text='ping'),
                    MessageAction(label='Translate Rice', text='米')
                ])
            template_message = TemplateMessage(
                alt_text='Buttons alt text',
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
    am = ActionManager(line_bot_api)

    am.send_or_pick('U5169a71261da89a47ad319b722f5c7e5')
#am.onboard_date('U5169a71261da89a47ad319b722f5c7e5')
