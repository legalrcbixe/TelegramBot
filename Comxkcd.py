#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the xkcd command from the bot

import random
import requests

xkcd_newest_url = 'http://xkcd.com/info.0.json'


def get_newest_xkcd_number():
    """
    Gets the number of the newest xkcd comic
    :return: int - number of the newest xkcd comic
    """
    xkcd_newest_response = requests.get(xkcd_newest_url).json()
    return xkcd_newest_response['num']


def get_xkcd_link():
    """
    Returns a randon xkcd comic
    :return: string - link to the imgage file of xkcd comic
    """
    rnd_number = random.randrange(1,get_newest_xkcd_number()) #get a random number, using newest xkcd as upper limit
    request_string = 'http://xkcd.com/{}/info.0.json'.format(rnd_number)
    xkcd_rnd_response = requests.get(request_string).json()
    return xkcd_rnd_response['img']
