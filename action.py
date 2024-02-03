from linebot.models import MessageAction, TemplateSendMessage, ConfirmTemplate, ButtonsTemplate, PostbackAction, DatetimePickerAction

class ActionManager():

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api

    def send_or_pick(self, user_id):
        print("Send or Pick")
        self.line_bot_api.push_message(user_id, TemplateSendMessage(
            alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    text='送機 or  接機',
                    actions=[
                        PostbackAction(
                            label='送機',
                            data='send_postback'
                        ),
                        PostbackAction(
                            label='接機',
                            data='pick_postback'
                        ),
                        PostbackAction(
                            label='取消',
                            data='cancel_postback'
                        )
                    ]
                )
            ))

    def send_answer(self, user_id)
        pass

    def onboard_date(self, user_id):
        self.line_bot_api.push_message(user_id, TemplateSendMessage(
            alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    text='接送機時間',
                    actions=[
                        DatetimePickerAction(
                            label='時間',
                            data='datetime_postback',
                            mode='datetime'
                        ),
                        PostbackAction(
                            label='取消',
                            data='取消'
                        )
                    ],
                )
            ))

    def get_name(self, user_id):
        self.line_bot_api.push_message(user_id, TemplateSendMessage(
            alt_text='ButtonsTemplate',
                template=ButtonsTemplate(
                    text='接送機時間',
                    actions=[
                        DatetimePickerAction(
                            label='時間',
                            data='datetime_postback',
                            mode='datetime'
                        ),
                        PostbackAction(
                            label='取消',
                            data='取消'
                        )
                    ],
                )
            ))
