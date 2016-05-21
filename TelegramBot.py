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

commands_clean = {'help' : 'Gibt eine Liste der Befehle aus',
                'time' : 'Gibt die aktuelle Zeit in Berlin, Tokio, Los Angeles und Shanghai aus',
                'fu' : 'Postet das "Fuck You" Bild',
                'remind' : 'Gibt einen Erinnerungstext nach einer definierten Zeit aus. Nutzung:\n/remind H M Erinnerungstext...'}

commands_dirty = {'tdt' : 'Posted das aktuelle Titten des Tages Bild',
                    'boobs' : 'Postet ein zufälliges Bild von oboobs.ru',
                    'butts' : 'Postet ein zufälliges Bild von obutts.ru'}

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ComTime, ComTdT, ComOPorn
import logging, os



# Enable logging
logging.basicConfig(
        filename='tgbot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

temp_img_dir = './Images/temp'
jobs = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update, args):
    if len(args) > 1 or len(args) < 0:
        bot.sendMessage(update.message.chat_id, text="Bitte nur ein Argument angeben")
    if args:
        if {**commands_clean, **commands_dirty}.get(args[0]) is not None:
            bot.sendMessage(update.message.chat_id, text={**commands_clean, **commands_dirty}[args[0]])
        else:
            bot.sendMessage(update.message.chat_id, text="Keine C.A.B.A.L. Funktion")
    else:
        command_list = ""
        if update.message.chat_id == -5707720:
            for key in commands_dirty:
                command_list += key + '\n'
        for key in commands_clean:
            command_list += key + '\n'
        bot.sendMessage(update.message.chat_id, text=command_list)


def time(bot, update):
    bot.sendMessage(update.message.chat_id, text=ComTime.return_time_msg())


def tdt(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=ComTdT.get_tdt_img_url())


def fu(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=open('./Images/media/Fuck_you.jpg', 'rb'))


def boobs(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_oboobs_url())


def butts(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_obutts_url())


def remind(bot, update, args):
    if len(args) < 2:
        bot.sendMessage(update.message.chat_id, text="Bitte zwei Argumente nutzen: Stunden Minuten Erinnerung...")
    try:
        int(args[0])
        int(args[1])
    except ValueError:
        bot.sendMessage(update.message.chat_id, text="Als erstes bitte die Zeit in Stunden, dann die Zeit in Minuten \
                                                     angeben: H M Nachricht...")
    delay = int(args[0]) * 3600 + int(args[1]) * 60
    remind_message = ' '.join(args[2:])

    # inner alarm function
    def reminder(bot):
        bot.sendMessage(update.message.chat_id, text=remind_message)

    jobs.put(reminder, delay, repeat=False)
    bot.sendMessage(update.message.chat_id, text="Erinnerung in {}h {}m".format(args[0], args[1]))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global jobs
    # Get bot token from token.conf
    with open("token.conf") as token_file:
        bot_token = str(token_file.readline())

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=bot_token)
    jobs = updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help, pass_args=True))

    # custom commands
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("tdt", tdt))
    dp.add_handler(CommandHandler("fu", fu))
    dp.add_handler(CommandHandler("boobs", boobs))
    dp.add_handler(CommandHandler("butts", butts))
    dp.add_handler(CommandHandler("remind", remind, pass_args=True))

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
