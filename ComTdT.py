#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the tdt command from the bot

from bs4 import BeautifulSoup
import urllib.request


def get_tdt_img_url():
    """
    Finds the image url of the newest TdT picture
    :return: string - url of the image
    """
    tdt_url = urllib.request.urlopen('http://tittendestages.tumblr.com/')
    tdt_soup = BeautifulSoup(tdt_url, "html.parser")
    img_soup = tdt_soup.find("divabc", class_="post photo").a.img.attrs['src']
    img_url = str(img_soup)
    return img_url
