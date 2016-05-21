#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A telegram group bot based on echobot2:
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py

"""
This Bot uses the Updater class to handle the bot.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ComTime, ComTdT
import logging, os

# Enable logging
logging.basicConfig(
        filename='tgbot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

temp_img_dir = './Images/temp'


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def time(bot, update):
    bot.sendMessage(update.message.chat_id, text=ComTime.return_time_msg())


def tdt(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=ComTdT.get_tdt_img_url())

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Get bot token from token.conf
    with open("token.conf") as token_file:
        bot_token = str(token_file.readline())

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # custom commands
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("tdt", tdt))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
