#!/usr/bin/env python
# encoding: utf-8
"""
Simple script to find extremes from weather data given by yr.no using our
previously written weather functions.

The script attempts to find the hottest and the coldest temperatures in a small
subset of Norwegian places (we limit it to 100 forecast requests to not spam
yr.no too much) at the next 13:00.

As a note it would probably be easier to just use the weather data given by
fetch_forecast(), however this also works.
"""
import weather
import re

if __name__ == "__main__":
    # Get forecast string for as many places as we can (100).
    forecast = weather.weather_update("*", 13, 00)

    # Regexp string and get location names and temperatures.
    # Iterate over matches and determine the hottest and the coldest location.
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

    # Print results.
    print "At next 13:00"
    print "Hottest: {} at {} C".format(hottest[0], hottest[1])
    print "Coldest: {} at {} C".format(coldest[0], coldest[1])
