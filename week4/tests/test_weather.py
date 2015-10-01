#!/usr/bin/env python
# encoding: utf-8
from .. import weather
from .. import weatherbuf
import re
from datetime import datetime, timedelta
import time
import os


def test_get_url():
    f = open("tests/islostarepeat.html", "r")
    s1 = f.read()
    s2 = weather.get_url("http://www.islostarepeat.com")
    assert s1 == s2


def test_find_location_links():
    links = weather.find_location_links("Hannestad")
    assert "http://www.yr.no/place/Norway/Østfold/Sarpsborg/Hannestad/" \
           "forecast.xml".decode("utf-8") in links


def test_hannestad_temperature():
    """
    Tests the temperature in Hannestad. Ensures it's between -50 and 50.
    Since forecast.xml does not provide any data about the current time,
    it will test the values one hour from now.
    """
    cur_time = datetime.now() + timedelta(hours=1)
    f = weather.weather_update("Hannestad", cur_time.hour, cur_time.minute)
    t = re.findall(r"temp\:(\S*)", f)
    t = int(t[0])
    assert -50 < t < 50


def test_hannestad_temperature_1300():
    """
    Tests the temperature in Hannestad. Ensures it's between -50 and 50 at
    1300.
    """
    f = weather.weather_update("Hannestad", 13, 00)
    t = re.findall(r"temp\:(\S*)", f)
    t = int(t[0])
    assert -50 < t < 50


def buffer_func(arg):
    """
    Test function for usage with buffer tests.
    """
    print "From func"
    return arg


def test_buffer_basic(capsys):
    """
    Tests if buffer initially reads from function and then subsequently reads
    from buffer.
    """
    arg = "test"
    if os.path.exists(weatherbuf.CACHE_PATH + arg + ".tmp"):
        os.remove(weatherbuf.CACHE_PATH + arg + ".tmp")

    func = weatherbuf.WeatherBuf(buffer_func)

    # Test to see that the buffer will only get the value from the function
    # once.
    func(arg)
    out, err = capsys.readouterr()
    assert out == "From func\n"
    func(arg)
    out, err = capsys.readouterr()
    assert out == ""
    os.remove(weatherbuf.CACHE_PATH + arg + ".tmp")


def test_buffer_timestamp(capsys):
    """
    Tests if buffer with timestamps to see if buffer works as intended.
    """
    arg = "test"
    if os.path.exists(weatherbuf.CACHE_PATH + arg + ".tmp"):
        os.remove(weatherbuf.CACHE_PATH + arg + ".tmp")

    old_timestamp = int(time.time()) - 14400  # Four hours old
    new_timestamp = int(time.time()) + 14400  # Four hours into the future
    func_old = weatherbuf.WeatherBuf(buffer_func, old_timestamp)
    func_new = weatherbuf.WeatherBuf(buffer_func, new_timestamp)

    # Test to see that the buffer will replace if the current file is old.
    func_old(arg)
    out, err = capsys.readouterr()
    assert out == "From func\n"
    func_new(arg)
    out, err = capsys.readouterr()
    assert out == "From func\n"

    # Clean up
    os.remove(weatherbuf.CACHE_PATH + arg + ".tmp")

    # Test to see that the buffer will not replace if the current file is new.
    func_new(arg)
    out, err = capsys.readouterr()
    assert out == "From func\n"
    func_old(arg)
    out, err = capsys.readouterr()
    assert out == ""
