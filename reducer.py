#!/usr/bin/env python

import sys


# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    print line.strip()
