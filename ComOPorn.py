#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the oboobs and obutts commands from the bot
import requests

max_boobs = 10568
max_butts = 3630


def return_oboobs_url():
    new_boob = requests.get('http://api.oboobs.ru/noise/1').json()
    oboobs_url = 'http://media.oboobs.ru/' + new_boob[0]['preview']
    return oboobs_url


def return_obutts_url():
    new_butt = requests.get('http://api.obutts.ru/noise/1').json()
    obutts_url = 'http://media.obutts.ru/' + new_butt[0]['preview']
    return obutts_url
