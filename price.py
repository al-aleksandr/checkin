"""
Prices
"""

secInMinuet = 60.0
secInHour = 60.0*secInMinuet

# FreeTimeInSec - count of seconds which 
FreeTimeInSec = 10.0*secInMinuet

firstHourPriceUAH = 45.0
nextHourPriceUAH  = 40.0
dayPriceUAH       = 190.0

SalePrice = {
    "Tea"               : 7,
    "Coffee"            : 12,
    "Eko Candy"         : 3,
    "Coffee with Milk"  : 14,
    "Tea Premium"       : 21,
    }

def getPrice(timeInSec):
    if timeInSec < FreeTimeInSec:
        return 0
    if timeInSec <= secInHour:
        price = firstHourPriceUAH
    else:
        price = firstHourPriceUAH + ((timeInSec - secInHour)*nextHourPriceUAH)/secInHour
    if price > dayPriceUAH:
        price = dayPriceUAH
    return int(price)

def getSalePrice(Name):
    return int(SalePrice.get(Name, 0))
