#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import datetime
from PIL import Image, ImageFont, ImageDraw

EPD_WIDTH = 640
EPD_HEIGHT = 384
x_margin = 32
y_padding = 25
y_margin = 15
x_padding = 15


def get_atlanta_json():
    json = None
    while json is None:
        print("retrying atlanta")
        try:
            data = requests.get("https://api.weather.gov/points/33.896284360721175,-84.445948540257", timeout=0.5)
            return data.json()
        except:
            pass


def get_hourly_data(url):
    json = None
    while json is None:
        print("retrying hourly")
        try:
            data = requests.get(url, timeout=0.5)
            json = data.json()
            return json
        except:
            pass


def get_time_string(hour):
    if hour == 0:
        return str(12) + " AM"
    elif hour < 12:
        return str(hour) + " AM"
    elif hour == 12:
        return str(hour) + " PM"
    else:
        return str(hour - 12) + " PM"


def get_image_from_string(string, chance, hour):
    Himage = Image.new('1', (100, 125), 255)
    if string == "Slight Chance Rain Showers":
        img = Image.open('rain.png')
    elif string == "Chance Rain Showers":
        img = Image.open('rain.png')
    elif string == "Rain Showers Likely":
        img = Image.open('rain.png')
    elif string == "Rain Showers":
        img = Image.open('rain.png')
    elif string == "Showers And Thunderstorms Likely":
        img = Image.open('storm.png')
    elif string == "Showers And Thunderstorms":
        img = Image.open('storm.png')
    elif string == "Mostly Cloudy":
        img = Image.open('cloud.png')
    elif string == "Cloudy":
        img = Image.open('cloud.png')
    elif string == "Patchy Fog":
        img = Image.open('cloud.png')
    elif 20 > hour >= 6:
        if string == "Chance Showers And Thunderstorms":
            img = Image.open('partly_thunder.png')
        elif string == "Mostly Clear":
            img = Image.open('partly.png')
        elif string == "Mostly Sunny":
            img = Image.open('sun.png')
        elif string == "Partly Sunny":
            img = Image.open('partly.png')
        elif string == "Sunny":
            img = Image.open('sun.png')
        elif string == "Slight Chance Showers And Thunderstorms":
            img = Image.open('partly_thunder.png')
        elif string == "Partly Cloudy":
            img = Image.open('partly.png')
        elif string == "Clear":
            img = Image.open('sun.png')
        else:
            print("Found an option I do not recognize:", string)
            img = Image.open('sun.png')
    else:
        if string == "Chance Showers And Thunderstorms":
            img = Image.open('partly_thunder_moony.png')
        elif string == "Mostly Clear":
            img = Image.open('partly_moony.png')
        elif string == "Mostly Sunny":
            img = Image.open('moon.png')
        elif string == "Partly Sunny":
            img = Image.open('partly_moony.png')
        elif string == "Sunny":
            img = Image.open('moon.png')
        elif string == "Slight Chance Showers And Thunderstorms":
            img = Image.open('partly_thunder_moony.png')
        elif string == "Partly Cloudy":
            img = Image.open('partly_moony.png')
        elif string == "Clear":
            img = Image.open('moon.png')
        else:
            print("Found an option I do not recognize:", string)
            img = Image.open('moon.png')

    Himage.paste(img, (0, 0))

    if chance > 0:
        chance_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 24)
        draw = ImageDraw.Draw(Himage)
        draw.text((20, 95), str(chance) + "%", font=chance_font)

    return Himage


def get_weather_image(reloads, message):
    try:
        reloads_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 12)
        message_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 20)
        weather_time_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 18)
        heading_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 25)
    except:
        reloads_font = ImageFont.load_default()
        message_font = ImageFont.load_default()
        weather_time_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
    json = get_atlanta_json()
    hourly_json = get_hourly_data(json['properties']['forecastHourly'])
    periods = hourly_json['properties']['periods']
    Himage = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((x_margin, y_margin), "Weather Forecast for " + str(datetime.datetime.now().strftime("%A, %B %d")), font=heading_font)
    lastx = x_margin
    lasty = 70
    weather_types = {}
    for i in range(0, 10):
        period = periods[i]
        start = datetime.datetime.strptime(period['startTime'][:-6], '%Y-%m-%dT%H:%M:%S')
        # end = datetime.datetime.strptime(period['endTime'], '%Y-%m-%dT%H:%M:%S-04:00')
        url = period['icon']
        comma = url.find(',')
        question = url.find('?')
        chance = 0
        if comma is not None and comma != -1:
            chance = int(url[comma + 1:question])
        if period['shortForecast'] in weather_types:
            weather_types[period['shortForecast']] += 1
        else:
            weather_types[period['shortForecast']] = 1
        img = get_image_from_string(period['shortForecast'], chance, start.time().hour)
        if lastx + img.width >= EPD_WIDTH - x_margin:
            lasty += img.height + y_padding
            lastx = x_margin
        Himage.paste(img, (lastx, lasty))
        time = get_time_string(start.time().hour)
        draw.text((lastx + 10, lasty - 15),
                  time + "   " + str(period['temperature']) + 'F',
                  font=weather_time_font, fill=0)
        lastx += img.width + x_padding
    # print weather_types
    draw.text((5, 5), str(reloads), font=reloads_font)
    draw.text((x_margin, EPD_HEIGHT - 2 * y_margin), message, font=message_font)
    return Himage


if __name__ == '__main__':
    get_weather_image(200, "TEST").show()
