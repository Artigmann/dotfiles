from urllib import urlopen


def get_url(url):
    f = urlopen(url)
    s = f.read()
    f.close()
    return s

if __name__ == "__main__":
    s = get_url("http://www.islostarepeat.com")
    print s
