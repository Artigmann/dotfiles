#!/usr/bin/env python
# encoding: utf-8
from urllib import urlopen
from time import strptime
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


def find_locations_yr_no(location):
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
    fetch = weathercache.WeatherCache(get_url)
    content = fetch(url)

    #name = re.search(r"\<name\>(.*)\<\/name\>", content).group(1)
    name = re.search(re_name, content).group(1)
    print "Name: " + name

    data = re.findall(re_forecast, content)
    print "Data found."
    time_str = "%Y-%m-%dT%H:%M:%S"

    # List comprehension should be here instead
    lst = []
    for f in data:
        time_from = strptime(f[0], time_str)
        time_to = strptime(f[1], time_str)
        symbol = f[2]
        precipitation = float(f[3])
        windspeed = float(f[4])
        temperature = int(f[5])
        lst.append([time_from, time_to, symbol, precipitation, windspeed,
                    temperature])

    return (name, lst)


if __name__ == "__main__":
    print "lol, no main"
    # find_location_links()
