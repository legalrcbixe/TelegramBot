#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the kicktipp command from the bot

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request


def get_creds():
    creds = []
    with open('./res/kicktipp.conf') as kicktipp_creds:
        for i, line in enumerate(kicktipp_creds):
            creds.append(str(line).strip('\n'))
    return creds


def get_table(login, pwd, group):
    positions = []
    players = []
    scores = []
    browser = webdriver.PhantomJS()
    browser.get("https://www.kicktipp.de/")
    browser.find_element_by_id('kennung').send_keys(login)
    browser.find_element_by_id('passwort').send_keys(pwd)
    browser.find_element_by_name('submitbutton').click()
    browser.get('https://www.kicktipp.de/{}/gesamtuebersicht'.format(group))
    names = browser.find_elements_by_class_name('mg_class')
    for name in names:
        players.append(str(name.text))

    points = browser.find_elements_by_class_name('pkt')
    for i, point in enumerate(points):
        if ((i+1) % 3) == 0:
            scores.append(str(point.text))
    spots = browser.find_elements_by_class_name('pos')
    for spot in spots:
        positions.append(spot.text)
    browser.quit()
    return positions, players, scores


def get_kicktipp_msg():
    creds = get_creds()
    kicktipp_msg = "https://www.kicktipp.de/emheuteabend/\n{:>3}  {:<10}  {:>6}\n".format("Pos", "Name", "Punkte")
    positions, players, scores = get_table(creds[0], creds[1], creds[2])
    for i, stats in enumerate(players):
        line = "{:>3}  {:<13}  {:>6}\n".format(positions[i], players[i], scores[i])
        kicktipp_msg += line
    return kicktipp_msg

def main():
    print(get_kicktipp_msg())


if __name__ == '__main__':
    main()