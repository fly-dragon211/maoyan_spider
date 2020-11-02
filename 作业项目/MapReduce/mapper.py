#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        print('%s\t%s' % (word.lower(), 1))