#!/usr/bin/python

from datetime import datetime, timedelta
from urllib2 import urlopen
import time
import random
import httplib

#pageurl = 'http://ars.userfriendly.org/cartoons/?id='
# Now that Userfriendly is offline, the cartoonarchive only exists on archive.org
pageurl = 'https://web.archive.org/web/20220225091531/http://ars.userfriendly.org/cartoons/?id='
fromstr = '<img border="0" src="'
tostr = '"'

import os
import os.path

def download_comic(dt):
  try:
    id = str(dt.date()).replace("-", "")
    while True:
      try:
        f = urlopen(pageurl + id).read()
        break
      except:
        time.sleep(60)
        pass
    ifrom = f.find(fromstr) + len(fromstr)
    url = f[ifrom: f.find(tostr, ifrom + 1)]
    if url == 'error':
      print("Strip %s (%s) doesn't exist" % (pageurl, str(dt)))
      return True
    ext = url[url.rfind("."):]

    os.chdir(os.path.dirname(__file__))
    path = "%d" % dt.year
    if not os.path.exists(path) or (os.path.exists(path) and not os.path.isdir(path)):
      try:
        os.mkdir(path)
      except:
        print("Could not create target directory, aborting.")
        exit()

    f = open("%d/%s%s" % (dt.year, id, ext), "wb")
    f.write(urlopen(url).read())
    f.close()
    return True
  except httplib.IncompleteRead:
    print("Error while downloading %s (%s). Please retry." % (pageurl, str(dt)))
    return False


def download_archive():
  dt = datetime(year=1997, month=11, day=17)
  delta = timedelta(days=1)
  while dt <= datetime.now():
    if download_comic(dt):
      dt += delta
    # Wait for a while as not to hammer UF servers
    time.sleep(6 * random.random())


def download_current():
  dt = datetime.now()
  download_comic(datetime.now())

def show_help():
  print("""Usage:
./uf-download.py archive     // Download the WHOLE UserFriendly webcomic archive
./uf-download.py current     // Download the current comic strip
./uf-download.py help        // Show this message

Important! Please see the README file for legal hints & other useful information.
""")

from sys import argv

def main():
  if len(argv) > 1:
    if argv[1] == "current":
      download_current()
    elif argv[1] == "archive":
      download_archive()
    else:
      show_help()
  else:
    show_help()


if __name__ == "__main__":
    main()
