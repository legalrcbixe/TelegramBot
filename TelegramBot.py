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
import ComTime
import ComTdT
import ComOPorn
import Comxkcd
import ComUtils
import ComKicktipp
import logging
import time

commands_clean = {'help': 'Gibt eine Liste der Befehle aus',
                    'time': 'Gibt die aktuelle Zeit in Berlin, Tokio, Los Angeles und Shanghai aus',
                    'fu': 'Postet das "Fuck You" Bild',
                    'remind': 'Gibt einen Erinnerungstext nach einer definierten Zeit aus. Nutzung:\n/remind H M Erinnerungstext...',
                    'code': 'Postet den Link zur GitHub Repository des C.A.B.A.L. Bots',
                    'wish': 'Postet den Bearbeiterlink zum GDoc der Wunschfunkionen des Bots. Bitte nur die Felder Funktion, Name und Priorität ausfüllen.',
                    'xkcd': 'Postet einen zufälligen xkcd Comic',
                    'chatid': 'Gibt die ChatId des aktuellen Chats aus',
                    'watn': 'Postet das "Was ist den los mit dir" Bild',
                    'bier': 'Postet ein Gif von Bier',
                    'kicktipp': 'Postet den Link zur "Heute Abend EM Kicktipptruppe und gibt den aktuellen Punktestand aus'}

commands_dirty = {'tdt' : 'Posted das aktuelle Titten des Tages Bild',
                    'boobs': 'Postet ein zufälliges Bild von oboobs.ru',
                    'butts': 'Postet ein zufälliges Bild von obutts.ru',
                    'safemode': 'Schaltet/Deaktiviert den Bot für die Nutzung der NSFW Kommandos frei',
                    'bb': 'Sendet ein Boob und ein Butt Bild von oboobs.ru und obutts.ru',
                    'faptime': 'Sendet je 6 Boob und Butt Bilder von oboobs.ru und obutts.ru'}

img_media_dir = './Images/media/'
img_temp_dir = './Images/temp/'
res_dir = './res/'
bot_token = ""
dev_chat = 0
whitelist = []
safemode_list = []


# Enable logging
logging.basicConfig(
        filename=res_dir+'tgbot.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

jobs = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update, args):
    if update.message.chat_id in whitelist:
        if len(args) > 1 or len(args) < 0:
            bot.sendMessage(update.message.chat_id, text="Bitte nur ein Argument angeben")
        if args:
            if {**commands_clean, **commands_dirty}.get(args[0]) is not None:
                bot.sendMessage(update.message.chat_id, text={**commands_clean, **commands_dirty}[args[0]])
            else:
                bot.sendMessage(update.message.chat_id, text="Keine C.A.B.A.L. Funktion")
        else:
            command_list = ""
            if update.message.chat_id in safemode_list:
                for key in commands_dirty:
                    command_list += key + '\n'
            for key in commands_clean:
                command_list += key + '\n'
            bot.sendMessage(update.message.chat_id, text=command_list)


def time(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text=ComTime.return_time_msg())


def tdt(bot, update):
    if update.message.chat_id in whitelist and update.message.chat_id in safemode_list:
        bot.sendPhoto(update.message.chat_id, photo=ComTdT.get_tdt_img_url())


def fu(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendPhoto(update.message.chat_id, photo=open(img_media_dir+'Fuck_you.jpg', 'rb'))


def boobs(bot, update):
    if update.message.chat_id in whitelist and update.message.chat_id in safemode_list:
        bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_oboobs_url())


def butts(bot, update):
    if update.message.chat_id in whitelist and update.message.chat_id in safemode_list:
        bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_obutts_url())


def remind(bot, update, args):
    if update.message.chat_id in whitelist:
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


def code(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text="https://github.com/Gronner/TelegramBot")


def wish(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text="https://docs.google.com/spreadsheets/d/1DOgpUypLGMSrgVRmye5Q_EPZdIS07-Sd-GuqzX8e-5c/edit?usp=sharing")


def xkcd(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendPhoto(update.message.chat_id, photo=Comxkcd.get_xkcd_link())


def chatid(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.chat_id)


def maintenance(bot, update, args):
    if update.message.chat_id == dev_chat:
        if len(args) != 1:
            bot.sendMessage(chat_id=dev_chat, text="Bitte nur die Downtime in Stunden angeben.")
        else:
            try:
                int(args[0])
            except ValueError:
                bot.sendMessage(chat_id=dev_chat, text="Die Downtime in Stunden bitte als Ganzzahl angeben.")
                return
            with open(res_dir+'whitelist.conf') as whitelist:
                for i, line in enumerate(whitelist):
                    bot.sendMessage(chat_id=int(str(line).strip('\n')), text="Der Bot ist wegen Wartungsarbeiten für {} Stunde(n) nicht erreichbar!".format(int(args[0])))


def safemode(bot, update):
    global safemode_list
    if update.message.chat_id in whitelist:
        if update.message.chat_id in safemode_list:
            safemode_list.remove(update.message.chat_id)
            ComUtils.remove_from_safemode(safemode_list)
            safemode_list = ComUtils.get_safemode_list()
        else:
            ComUtils.add_to_safemode(update.message.chat_id)
            safemode_list = ComUtils.get_safemode_list()


def bb(bot, update):
    if update.message.chat_id in whitelist and update.message.chat_id in safemode_list:
        bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_oboobs_url())
        time.sleep(0.2)
        bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_obutts_url())


def faptime(bot, update):
    if update.message.chat_id in whitelist and update.message.chat_id in safemode_list:
        for i in range(0,6):
            bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_oboobs_url())
            bot.sendPhoto(update.message.chat_id, photo=ComOPorn.return_obutts_url())


def watn(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendPhoto(update.message.chat_id, photo=open(img_media_dir+'watn.png', 'rb'))


def bier(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text="https://media.giphy.com/media/92wsX8GEoNTYA/giphy.gif")


def kicktipp(bot, update):
    if update.message.chat_id in whitelist:
        bot.sendMessage(update.message.chat_id, text=ComKicktipp.get_kicktipp_msg())


def add(bot, update, args):
    global dev_chat
    global whitelist
    if len (args) != 1:
        bot.sendMessage(update.message.chat_id, text="Bitte nur die Chat ID als Argument angeben.")
    if update.message.chat_id == dev_chat:
        whitelist = ComUtils.add_to_whitelist(args[0])
        bot.sendMessage(update.message.chat_id, text="{} wurde zur whitelist hinzugefügt".format(args[0]))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global jobs
    global bot_token
    global dev_chat
    global whitelist
    global safemode_list
    # Get bot token and devchat from token.conf
    with open(res_dir + 'token.conf') as token_file:
        for i, line in enumerate(token_file):
            if i == 0:
                bot_token = str(line).strip('\n')
            if i == 1:
                dev_chat = int(str(line).strip('\n'))
                break

    whitelist = ComUtils.get_whitelist()
    safemode_list = ComUtils.get_safemode_list()

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
    dp.add_handler(CommandHandler("code", code))
    dp.add_handler(CommandHandler("wish", wish))
    dp.add_handler(CommandHandler("xkcd", xkcd))
    dp.add_handler(CommandHandler("chatid", chatid))
    dp.add_handler(CommandHandler("maintenance", maintenance, pass_args=True))
    dp.add_handler(CommandHandler("safemode", safemode))
    dp.add_handler(CommandHandler("bb", bb))
    dp.add_handler(CommandHandler("faptime", faptime))
    dp.add_handler(CommandHandler("watn", watn))
    dp.add_handler(CommandHandler("bier", bier))
    dp.add_handler(CommandHandler("kicktipp", kicktipp))
    dp.add_handler(CommandHandler("add", add, pass_args=True))

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
