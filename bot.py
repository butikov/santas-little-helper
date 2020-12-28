#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os
from model import Model
import settings


model = Model.from_pickles(settings.MODEL_FILE, settings.VECTORIZER_FILE)


def random_word(words):
    if len(words) > 0:
        return words[random.randint(0, len(words) - 1)].lower()
    else:
        return None


def send_meme(update, context):
    if update.message.text is None or update.message.text.startswith('/'):
        return
    update.message.reply_text(model.get_santa_answer(update.message.text))


def send_help(update, context):
    update.message.reply_text('2020 was very hard for Santa too. Tell this bot about your year and he will decide if '
                              'your deserve a present')


if __name__ == '__main__':
    updater = Updater(os.environ['TELEGRAM_TOKEN'], use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', send_help))
    updater.dispatcher.add_handler(CommandHandler('help', send_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, send_meme))

    updater.start_polling()
    updater.idle()
