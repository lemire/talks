from urllib.request import urlopen
from urllib.error import HTTPError

import timeit

def grab():
    try:
        data = urlopen("http://127.0.0.1:5000").read().decode("utf-8")
        return data
    except HTTPError:
        return None


t = timeit.timeit(grab, number=1000)


print (t)