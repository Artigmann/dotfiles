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


# TODO: Limit to maximum of 100?
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
def fetch_forecasts(url):
    content = get_url(url)

    name = re.search(r"\<name\>(.*)\<\/name\>", content).group(1)
    re_timestamp = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    re_time = r"<time.*?from\=\"(" + re_timestamp + r")\".*?to\=\"(" \
              + re_timestamp + r")\".*?>"
    re_symbol_name = r"<symbol.*?name\=\"(.*?)\".*?\/>"
    re_precipitation = r"<precipitation.*?value=\"(.*?)\".*?\/>"
    re_windspeed = r"<windSpeed.*?mps\=\"(.*?)\".*?\/>"
    re_temperature = r"<temperature.*?value\=\"(.*?)\".*?\/>"
    re_ending = r".*?<\/time>"
    re_all = re_time + r".*?" + re_symbol_name + r".*?" + re_precipitation \
                     + r".*?" + re_windspeed + r".*?" + re_temperature \
                     + re_ending

    data = re.findall(re_all, content, re.S)
    time_str = "%Y-%m-%dT%H:%M:%S"
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
    find_location_links()
