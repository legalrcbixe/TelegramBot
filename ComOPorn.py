#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the oboobs and obutts commands from the bot
import random
import urllib.request

max_boobs = 10568
max_butts = 3630

def return_oboobs_url():
    img_number = random.randrange(1,max_butts)
    oboobs_url = ''
    while True:
        oboobs_url = 'http://media.oboobs.ru/boobs/{0:05d}.jpg'.format(img_number)
        page = urllib.request.urlopen(oboobs_url)
        if page.getcode() == 200:
            break
        else:
            img_number += 1
    return oboobs_url


def return_obutts_url():
    img_number = random.randrange(1,max_butts)
    obutts_url = ''
    while True or img_number>10568:
        obutts_url = 'http://media.obutts.ru/butts/{0:05d}.jpg'.format(img_number)
        page = urllib.request.urlopen(obutts_url)
        if page.getcode() == 200:
            break
        else:
            img_number += 1
    print(obutts_url)
    return obutts_url
