#!/usr/bin/env python

from operator import itemgetter
import sys


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    file, el = line.split('=', 1)
    # convert count (currently a string) to int
    try:
        el = int(el)
        if el > 50:
            print "%s %d" % (file, el)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
