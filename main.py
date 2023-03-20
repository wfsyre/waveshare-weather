#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5
import time
import weather_reader
import traceback

reloads = 0


def get_text():
    f = open("message.txt")
    message = f.readline()
    return message


while(True):
    try:
        print("Waking up")
        Himage = weather_reader.get_weather_image(reloads, get_text())
        epd = epd7in5.EPD()
        epd.init()
        epd.Clear(0xFF)
        # Drawing on the Horizontal image
        epd.display(epd.getbuffer(Himage))
        reloads += 1
        time.sleep(2)
        epd.sleep()
        print("Going to sleep")
        time.sleep(60 * 30)
    except:
        print("Attempting to salvage")
        epd.init()
        epd.Clear(0xFF)
        epd.sleep()
        print("That's the best I got")
        time.sleep(4)
        print('traceback.format_exc():\n%s' % traceback.format_exc())

