#!/usr/bin/env python
# encoding: utf-8
from urllib import urlopen
from datetime import datetime, timedelta
import re
import weathercache

re_name = re.compile(r"<name>(.*?)<\/name>");
re_forecast = re.compile(r"""
        <time .*? from\=\" (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) \" # from timestamp
        .*? to\=\" (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) \" .*? >   # to timestamps
        .*?<symbol .*? name\=\" (.*?) \" .*? \/>                    # symbol name
        .*?<precipitation .*? value\=\" (.*?) \" .*? \/>            # precipitation value
        .*?<windSpeed .*? mps\=\" (.*?) \" .*? \/>                  # windspeed (mps)
        .*?<temperature .*? value\=\" (.*?) \" .*? \/>              # temperature value
        .*?<\/time>
        """, re.DOTALL | re.VERBOSE)

def get_url(url):
    """
    Returns content at given URL.
    """
    return urlopen(url).read().decode("utf-8")  # TODO: check encoding.


def find_location_links(location):
    """
    Returns a list of (max 100) XML links matching either stedsnavn, kommune or fylke in
    that order. Supports the typical command-line wildcard.
    """
    if location:
        # Escape the user given string and replace wildcards with .*
        search = re.sub("\\\\\*", "(?:\S| )*", re.escape(location))
    else:
        # Wildcard if there's no location string.
        search = r"(?:\S| )*"

    fetch = weathercache.WeatherCache(get_url)
    content = fetch("http://fil.nrk.no/yr/viktigestader/noreg.txt")

    re_opener = r"^\d+\t"
    re_kommune = r"(?:\S| )+\t\d+\t(?:\S| )+\t(?:\S| )+\t(?:\S| )+\t"
    re_xml = r"\t.+(http.+forecast.xml)"

    # Find stadnamn
    links = re.findall(re_opener + search + re_xml, content, re.M)
    if not links:
        # No stadnamn, find kommune
        links = re.findall(re_opener + re_kommune + search + re_xml, content, re.M)
        if not links:
            # No kommune, find fylke
            links = re.findall(re_opener + re_kommune + r"(?:\S| )+\t" + search +
                             re_xml, content, re.M)

    unique_links = []
    [unique_links.append(x) for x in links if x not in unique_links]
    return unique_links[0:100]



# TODO: Check if we need to add decode to strings.
#       Perhaps limit everything to the next 24 hours?
def fetch_forecasts(url):
    """
    Finds forecasts from given XML-file URL. Returns a list of lists with the
    name of the place and a list containing time_from, time_to, symbol name,
    precipitation, windspeed and temperature.
    """
    url = url.encode("utf-8")
    fetch = weathercache.WeatherCache(get_url)
    content = fetch(url)

    #name = re.search(r"\<name\>(.*)\<\/name\>", content).group(1)
    name = re.search(re_name, content).group(1)
    print "Name: {}".format(name.encode("utf-8"))

    data = re.findall(re_forecast, content)
    print "Data found."
    time_str = "%Y-%m-%dT%H:%M:%S"

    lst = [[datetime.strptime(i[0], time_str), datetime.strptime(i[1], time_str), i[2], float(i[3]), float(i[4]), int(i[5])] for i in data]
    return (name, lst)

def weather_update(location, hour, minute):
    location = location.decode("utf-8") # TODO: Fix encoding.
    links = find_location_links(location)

    next_slot = datetime.now().replace(minute=0) + timedelta(hours=1)
    target_time = datetime.now().replace(hour=hour, minute=minute)
    if target_time < next_slot:
        target_time += timedelta(days=1)

    string = "{}\n".format(target_time.strftime("%d.%m.%y %H:%M"))
    for l in links:
        forecasts = fetch_forecasts(l)
        name = forecasts[0].encode("utf-8")

        #if target_time < time_from:
        #    target_time += timedelta(day=1)

        for f in forecasts[1]:
            time_from = f[0]
            time_to = f[1]
            symbol = f[2]
            precipitation = f[3]
            windspeed = f[4]
            temperature = f[5]

            if target_time >= time_from and target_time < time_to:
                string += "{}: {}, rain:{:.1f} mm, wind:{:.1f} mps, temp:{} deg C\n" \
                           .format(name, symbol, precipitation, windspeed, temperature)
                break
    return string

if __name__ == "__main__":
    print "lol, no main"
    # find_location_links()
