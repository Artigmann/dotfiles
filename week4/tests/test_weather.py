from .. import weather


def test_get_url():
    f = open("tests/islostarepeat.html", "r")
    s1 = f.read()
    s2 = weather.get_url("http://www.islostarepeat.com")
    assert s1 == s2
