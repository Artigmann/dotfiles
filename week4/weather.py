#!/usr/bin/env python
# encoding: utf-8
from urllib import urlopen
import re


def get_url(url):
    """
    Returns content at given URL.
    """
    return urlopen(url).read()


def find_location_links(location):
    """
    Returns a list of XML links matching either stedsnavn, kommune or fylke in that order.
    Supports the typical command-line wildcard.
    """
    # Escape the user given string and replace wildcards with .*
    search = re.sub("\\\\\*", "(?:\S| )*", re.escape(location))
    content = get_url("http://fil.nrk.no/yr/viktigestader/noreg.txt")

    re_opener = r"^\d+\t"
    re_kommune = r"(?:\S| )+\t\d+\t(?:\S| )+\t(?:\S| )+\t(?:\S| )+\t"
    re_xml = r"\t.+(http.+forecast.xml)"

    # Finn stedsnavn
    links = re.findall(re_opener + search + re_xml, content, re.M)
    if links:
        return links

    # If not stedsnavn, find kommune
    links = re.findall(re_opener + re_kommune + search + re_xml, content, re.M)
    if links:
        return links

    # if not kommune, find fylke
    return re.findall(re_opener + re_kommune + r"(?:\S| )+\t" + search + re_xml, content, re.M)


def get_weather_data(url):
    content = get_url(url)

    name = re.search(r"\<name\>(.*)\<\/name\>", content).group(1)
    


if __name__ == "__main__":
    find_location_links()
