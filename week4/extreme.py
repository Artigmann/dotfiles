#!/usr/bin/env python
# encoding: utf-8
import weather
import re

if __name__ == "__main__":
    forecast = weather.weather_update("*", 13, 00)

    matches = re.finditer(r"^(.*?)\:.*?temp\:(\S*)", forecast, re.M | re.U)
    if matches:
        match = matches.next()
        hottest = (match.group(1), int(match.group(2)))
        coldest = (match.group(1), int(match.group(2)))
    for match in matches:
        name = match.group(1)
        temp = int(match.group(2))
        if temp > hottest[1]:
            hottest = (name, temp)
        elif temp < coldest[1]:
            coldest = (name, temp)

    print "At next 13:00"
    print "Hottest: {} at {} C".format(hottest[0], hottest[1])
    print "Coldest: {} at {} C".format(coldest[0], coldest[1])
