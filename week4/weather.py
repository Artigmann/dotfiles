#!/usr/bin/env python
# encoding: utf-8
"""
Module to fetch and parse data from yr.no. Can also be run with the following
arguments to fetch a specific forecast:
`python weather.py LOCATION HOUR MINUTE`
"""
from urllib import urlopen
from datetime import datetime, timedelta
from collections import namedtuple
import re
import weatherbuf
import sys

# RE to find name from XML file.
re_name = re.compile(r"<name>(.*?)<\/name>")
# RE to extract data from XML file.
re_forecast = re.compile(r"""
        # from timestamp
        <time .*? from\=\" (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) \"

        # to timestamps
        .*? to\=\" (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) \" .*? >

        # symbol name
        .*?<symbol .*? name\=\" (.*?) \" .*? \/>

        # precipitation value
        .*?<precipitation .*? value\=\" (.*?) \" .*? \/>

        # windspeed (mps)
        .*?<windSpeed .*? mps\=\" (.*?) \" .*? \/>

        # temperature value
        .*?<temperature .*? value\=\" (.*?) \" .*? \/>
        .*?<\/time>
        """, re.DOTALL | re.VERBOSE)


def get_url(url):
    """
    Returns content at given URL as string.
    """
    try:
        content = urlopen(url).read().decode("utf-8")
    except:
        return None
    return content


def find_location_links(location):
    """
    Returns a list of (max 100) XML links with location matching either
    stedsnavn, kommune or fylke in that order. Supports the typical
    command-line wildcard.
    """
    if location:
        # Escape the user given string and replace wildcards with .*
        search = re.sub("\\\\\*", "(?:\S| )*", re.escape(location))
    else:
        # Wildcard if there's no location string.
        search = r"(?:\S| )*"

    fetch = weatherbuf.WeatherBuf(get_url)
    content = fetch("http://fil.nrk.no/yr/viktigestader/noreg.txt")
    if not content:
        sys.stderr.write("Failed to retrieve index file (noreg.txt)\n")
        return None

    re_opener = r"^\d+\t"
    re_kommune = r"(?:\S| )+\t\d+\t(?:\S| )+\t(?:\S| )+\t(?:\S| )+\t"
    re_xml = r"\t.+(http.+forecast.xml)"

    # Find stadnamn
    links = re.findall(re_opener + search + re_xml, content, re.M | re.I)
    if not links:
        # No stadnamn, find kommune
        links = re.findall(re_opener + re_kommune + search + re_xml, content,
                           re.M | re.I)
        if not links:
            # No kommune, find fylke
            links = re.findall(re_opener + re_kommune + r"(?:\S| )+\t" +
                               search + re_xml, content, re.M | re.I)

    # Need to make the links unique, this is a fancy-ish of getting unique
    # links semi-fast while retaining the order.
    unique_links = []
    [unique_links.append(x) for x in links if x not in unique_links]
    return unique_links[0:100]


def fetch_forecasts(url):
    """
    Finds forecasts from given XML-file URL. Returns a tuple containing both
    name and a list of named tuples with time_from, time_to, symbol,
    precipitation, windspeed and temperature. Returns None if we fail to get
    URL or if content obviously doesn't match the requested XML-file.
    """
    url = url.encode("utf-8")
    fetch = weatherbuf.WeatherBuf(get_url)
    content = fetch(url)
    if not content:
        sys.stderr.write("Failed to retrieve URL: {}\n".format(url))
        return None

    name_match = re.search(re_name, content)
    if not name_match:
        sys.stderr.write("Failed to parse data from URL: {}\n".format(url))
        return None
    else:
        name = name_match.group(1)

    data = re.findall(re_forecast, content)
    time_str = "%Y-%m-%dT%H:%M:%S"

    Forecast = namedtuple("Forecast", ["time_from", "time_to", "symbol",
                          "precipitation", "windspeed", "temperature"])
    lst = [Forecast(datetime.strptime(i[0], time_str),
                    datetime.strptime(i[1], time_str), i[2], float(i[3]),
                    float(i[4]), int(i[5])) for i in data]
    return (name, lst)


def weather_update(location, hour, minute):
    """
    Gets weather forecast for given location at given time within the next
    24 hours. Location is the location we want the forecast for, this supports
    the typical command line wildcard. Hour and minute are the hour and the
    minute we want the forecast for. Returns a string containing the forecast.
    """
    location = location.decode("utf-8")
    links = find_location_links(location)
    if not links:
        return "Location \"{}\" not found.".format(location.encode("utf-8"))

    next_slot = datetime.now().replace(minute=0) + timedelta(hours=1)
    target_time = datetime.now().replace(hour=hour, minute=minute)
    if target_time < next_slot:
        target_time += timedelta(days=1)

    string = "{}".format(target_time.strftime("%d.%m.%y %H:%M"))
    for l in links:
        forecasts = fetch_forecasts(l)
        if not forecasts:
            continue
        name = forecasts[0].encode("utf-8")

        for f in forecasts[1]:
            if target_time >= f.time_from and target_time < f.time_to:
                string += "\n{}: {}, rain:{:.1f} mm, wind:{:.1f} mps, " \
                          "temp:{} deg C" \
                          .format(name, f.symbol, f.precipitation, f.windspeed,
                                  f.temperature)
                break
    return string


if __name__ == "__main__":
    """
    Give some basic functionality from the weather_update function.
    """
    if len(sys.argv) != 4:
        print "Usage: python {} location hour minute".format(sys.argv[0])
        sys.exit()
    location = sys.argv[1]
    try:
        hour = int(sys.argv[2])
        minute = int(sys.argv[3])
        if hour > 23 or hour < 0 or minute > 59 or minute < 0:
            raise ValueError
    except ValueError:
        print "Hour has to be an integer from 0 to 23, minute has to be an" \
              " integer from 0 to 59"
        sys.exit()
    print weather_update(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
