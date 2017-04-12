#! /usr/bin/env python
# -*- coding: utf-8 -*-


a = 'MVSTLPPCPQCNSEYTYEDGALLVCPECAHEWSPNEAATASDDGKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

b = range(0, 10000, 10)
b[0] = 1
for i in xrange((len(a)/10)+1):
    # je ne sais pas pourquoi ça ne marchait pas mais il a fallu faire 
    # comme ça
    if i == 0:
        print("{:<8d}".format(b[0])),
    else:
        print("{:<9d}".format(b[i])),
print("\n" + a)
