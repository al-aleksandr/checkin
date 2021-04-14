#! /usr/bin/env python
from smartcard.util import toHexString

def log(str):
	print(str)

def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def minPrice():
        return 30
    @constant
    def dayPrice():
        return 150

sw1 = 0
sw2 = 90
sw = [sw1, sw2]
log("Some error. Error code is %.2x %.2x" % (sw1, sw2))

log(toHexString(sw))

price = _Const()
print price.minPrice
print price.dayPrice