#!/usr/bin/python

from datetime import datetime, timedelta
from urllib2 import urlopen
import time
import random
import httplib

pageurl = 'http://ars.userfriendly.org/cartoons/?id='

fromstr = '<img border="0" src="'
tostr = '"'

dt = datetime(year=1997, month=11, day=17)
delta = timedelta(days=1)


while dt < datetime.now():
  try:
    id = str(dt.date()).replace("-", "")
    f = urlopen(pageurl + id).read()
    ifrom = f.find(fromstr) + len(fromstr)
    url = f[ifrom: f.find(tostr, ifrom + 1)]
    ext = url[url.rfind("."):]
    f = open("%s/%s%s" % (dt.year, id, ext), "wb")
    f.write(urlopen(url).read())
    f.close()
    time.sleep(6 * random.random())
    dt += delta
  except httplib.IncompleteRead:
    print("Error while downloading %s (%s)" % (pageurl, str(dt)))
    continue
