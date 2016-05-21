#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Manages the time command from the bot

from datetime import datetime
from pytz import timezone

timezones = ['UTC','Europe/Berlin', 'America/Los_Angeles', 'Asia/Shanghai', 'Asia/Tokyo']
time_format = '%H:%M:%S - %d.%m.%Y'

def return_time_str(tz):
    """
    Returns a string with the current time in the specified timezone
    :param timezone: string - Timezone name: Region/City
    :return: string - Place: HH:MM:SS DD.MM.YYYY
    """
    time_str = datetime.now(timezone(tz)).strftime(time_format)
    return time_str


def return_time_msg():
    """
    Returns a message string, containing the timezone data for timezones specified in timezones
    :return: string - Region: Time - Date \n ...
    """
    time_message = ""
    for tz in timezones:
        time_message += "{} | {}\n".format(return_time_str(tz), tz.replace("_", " "))
    return time_message
