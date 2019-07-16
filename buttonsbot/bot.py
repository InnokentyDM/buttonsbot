import telepot
from django.conf import settings
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from buttonsbot.models import BotUsers, MessageButton
from buttonsbot.utils import get_object_or_none


class ButtonMailBot(object):
    __bot = None
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if not ButtonMailBot.__instance:
            ButtonMailBot()
        return ButtonMailBot.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if not ButtonMailBot.__instance:
            ButtonMailBot.__instance = self
            ButtonMailBot.__instance.__bot = telepot.Bot(settings.BOT_TOKEN)
            MessageLoop(ButtonMailBot.__instance.__bot, {'chat': self.on_chat_message,
                                                         'callback_query': self.on_callback_query}).run_as_thread()

    def send_message(self, chat_id, msg, buttons={}, photo=None):
        keyboard_buttons = []
        for key, value in buttons.items():
            keyboard_buttons.append(InlineKeyboardButton(text=key, callback_data=value))

        keyboard = InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])
        if photo:
            self.__bot.sendPhoto(chat_id, photo, msg, reply_markup=keyboard)
        else:
            self.__bot.sendMessage(chat_id, msg, reply_markup=keyboard)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot_user, created = BotUsers.objects.get_or_create(chat_id=chat_id)
        if created:
            bot_user.username = msg['from']['username']
            bot_user.save()
        if content_type == 'text' and msg['text'] == '/start':
            self.__instance.send_message(chat_id, 'Привет {}'.format(bot_user.username))

    def on_callback_query(self, call_back_data):
        query_id, from_id, query_data = telepot.glance(call_back_data, flavor='callback_query')

        button = get_object_or_none(MessageButton, id=query_data)
        if button:
            button.click_count += 1
            button.save()
            self.__bot.answerCallbackQuery(query_id, text='Ваш ответ {} принят и записан'.format(button.name))
            user = get_object_or_none(BotUsers, chat_id=from_id)
            if user:
                user.last_pressed_button = button
                user.notification_count = 0
                user.save()
        else:
            self.__bot.answerCallbackQuery(query_id, text='Ошибка, ответ не был записан')

