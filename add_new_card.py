#! /usr/bin/env python
"""
Add new card to Data Base
"""
from __future__ import print_function
from time import sleep

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

import copy
import datetime

import database, processcard

# Get UID
APDU_GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x0A]


timeFormat = "%H:%M:%S  %a %d %b"
ListofNewCards = []
ListofCheckin = {}

def log(str):
    print(str)

def getNewCardItemPrimary(uid):
    card = {uid : datetime.datetime.now()}
    return card

def readCardUID(card):
    card.connection = card.createConnection()
    card.connection.connect()
    uid, sw1, sw2 = card.connection.transmit(
        APDU_GET_UID)
    if sw1 != 0x90 or sw2 != 0x00:
        log("Some error. Error code is %.2x %.2x" % (sw1, sw2))
        return None
    return toHexString(uid)


class transmitobserver(CardObserver):
    """A card observer that is notified when cards are inserted/removed
    from the system, connects to cards and SELECT DF_TELECOM """

    def __init__(self):
        self.cards = []

    def update(self, observable, actions):
        global ListofNewCards
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards += [card]
                uid = readCardUID(card)
                if uid == None:
                    log("Please insert card again")
                    return
                ListofNewCards.append(getNewCardItemPrimary(uid))

        for card in removedcards:
            if card in self.cards:
                self.cards.remove(card)

def AddNewCardToDB(newCard, num):
    print("Please set correct card values. \nExit beacause....")
    exit()
    global ListofCheckin
    log("")
    uid = newCard.keys()[0]
    print("UID: %s" %(uid))
    EmployeeName = processcard.CardTypeCoworker + " card #" + str(num)
    database.UpdateCard(uid, processcard.CardTypeCoworker, EmployeeName, "-", "Active", "31/12/20 10:30", processcard.CardTypeCoworker+"'s' card")

if __name__ == '__main__':
    log("Insert or remove a smartcard in the system.")
    log("")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)
    num = 0

    while True:
        while ListofNewCards == []:
            sleep(0.5)
        num += 1
        print("Card #%d" %num)
        AddNewCardToDB(ListofNewCards.pop(0), num)
