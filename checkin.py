#! /usr/bin/env python
"""
Checkin
"""
from __future__ import print_function
from time import sleep
import fcntl

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

import os.path
import tempfile
import sys
import copy
import datetime

import settings
import database
from processcard import processNewCard, PrintProcessCardResult, loadListofCheckin, ListofCheckinFileName
from logging import log, logd, loge, CreateLogFiles, saveLineToFile

# Get UID
APDU_GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x0A]


ListofNewCards = [] # Primary info. Cards are detected by reader

# Pid file to check one program instance 
fp_instance = 0

def isItAlreadyRunned(basename):
    global fp_instance
    pid_file = os.path.normpath(tempfile.gettempdir() + '/' + basename)
    fp_instance = open(pid_file, 'w')
    fp_instance.flush()
    try:
        fcntl.lockf(fp_instance, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # print("another instance is running")
        return True
    return False

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


if __name__ == '__main__':
    if isItAlreadyRunned('checkin.pid'):
        print("ERROR: A copy of program is runned already.")
        print("       Please use runned one or reboot PC")
        exit(0)

    CreateLogFiles()
    global ListofCheckinFileName
    loadListofCheckin(ListofCheckinFileName)
    
    log("Insert or remove a smartcard in the system.")
    log("")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)
    num = 0

    while True:
        while ListofNewCards == []:
            sleep(0.1)
        # TODO: Save ListofNewCards to file
        log("")
        PrintProcessCardResult(processNewCard(ListofNewCards.pop(0)))
        # TODO: Save ListofNewCards to file again
        log("------------------------------------------------------")
