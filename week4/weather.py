#!/usr/bin/env python
# encoding: utf-8
from urllib import urlopen
from time import strptime
import re


def get_url(url):
    """
    Returns content at given URL.
    """
    return urlopen(url).read().decode("utf-8")  # TODO: check encoding.


def find_location_links(location):
    """
    Returns a list of XML links matching either stedsnavn, kommune or fylke in
    that order. Supports the typical command-line wildcard.
    """
    # Escape the user given string and replace wildcards with .*
    search = re.sub("\\\\\*", "(?:\S| )*", re.escape(location))
    content = get_url("http://fil.nrk.no/yr/viktigestader/noreg.txt")

    re_opener = r"^\d+\t"
    re_kommune = r"(?:\S| )+\t\d+\t(?:\S| )+\t(?:\S| )+\t(?:\S| )+\t"
    re_xml = r"\t.+(http.+forecast.xml)"

    # Find stadnamn
    links = re.findall(re_opener + search + re_xml, content, re.M)
    if links:
        return links

    # If not stadnamn, find kommune
    links = re.findall(re_opener + re_kommune + search + re_xml, content, re.M)
    if links:
        return links

    # If not kommune, find fylke
    return re.findall(re_opener + re_kommune + r"(?:\S| )+\t" + search +
                      re_xml, content, re.M)


# TODO: Check if we need to add decode to strings.
def get_weather_data(url):
    content = get_url(url)

    name = re.search(r"\<name\>(.*)\<\/name\>", content).group(1)
    re_timestamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    re_time = r"<time from\=\"(" + re_timestamp + r")\"\s*?to\=\"(" \
              + re_timestamp + r")\".*?>"
    re_symbol_name = r"<symbol.*?name\=\"(.*?)\".*?\/>"
    re_precipitation = r"<precipitation value=\"(\d+)\".*?\/>"
    re_temperature = r"<temperature.*?value\=\"(\d+)\".*?\/>"
    re_all = re_time + r".*?" + re_symbol_name + r".*?" + re_precipitation \
                     + r".*?" + re_temperature

    data = re.findall(re_all, content, re.S)
    forecast = Forecast(name)
    time_str = "%Y-%m-%dT%H:%M:%S"
    for f in data:
        time_from = strptime(f[0], time_str)
        time_to = strptime(f[1], time_str)
        symbol = f[2]
        precipitation = int(f[3])
        temperature = int(f[4])
        forecast.add(time_from, time_to, symbol, precipitation, temperature)

    return forecast


class Forecast(object):
    def __init__(self, place):
        """
        Takes place as name of place the forecast is for.
        """
        self.place = place
        self._lst = []  # TODO: Should we use an inner class instead?

    def add(self, time_from, time_to, symbol, precipitation, temperature):
        self._lst.append([time_from, time_to, symbol, precipitation,
                         temperature])


if __name__ == "__main__":
    find_location_links()
