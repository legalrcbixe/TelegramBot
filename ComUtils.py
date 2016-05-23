#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the utility commands from the bot

res_dir = './res/'
whitelist_file = res_dir+'whitelist.conf'
safemode_file = res_dir+'safemode.conf'


def get_whitelist():
    whitelist = []
    with open(whitelist_file) as wf_file:
        for i, line in enumerate(wf_file):
            whitelist.append(int(str(line).strip('\n')))
    return whitelist


def get_safemode_list():
    safemode_list = []
    with open(safemode_file) as sf_file:
        for i, line in enumerate(sf_file):
            safemode_list.append(int(str(line).strip('\n')))
    return safemode_list


def add_to_safemode(chat_id):
    with open(safemode_file, 'a') as sf_file:
        sf_file.write(str(chat_id))


def remove_from_safemode(new_safemode_list):
    with open(safemode_file, 'w') as sf_file:
        for chat_id in new_safemode_list:
            sf_file.write("{}\n".format(chat_id))