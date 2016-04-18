# # -*- coding: utf-8 -*-

import os
import telegram

from telegram.ext import Updater

import config as cf


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):

    bot.sendAudio(chat_id=update.message.chat_id, audio=open(os.path.join(cf.FOLDER_TEMP, 'foo.ogg'), 'rb'))


token = '217941149:AAEXCQ1BSKwPrFxJjpebolwoMoDIsS-ZTlM'
bot = telegram.Bot(token=token)
updater = Updater(token=token)

dispatcher = updater.dispatcher
dispatcher.addTelegramCommandHandler('start', start)

updater.start_polling()

dispatcher.addTelegramMessageHandler(echo)
