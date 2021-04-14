#! /usr/bin/env python
"""
Sample script that monitors card insertions,
connects to cards and transmit an apdu

__author__ = "http://www.gemalto.com"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from __future__ import print_function
from time import sleep

# import smartcard
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

import copy
import datetime

# replace by your favourite apdu
APDU_DEFAULT = [0xA0, 0xA4, 0x00, 0x00, 0x02, 0x7F, 0x10]
# Get UID
APDU_GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x0A]

SELECT_DF_TELECOM = APDU_GET_UID

class cardinfo(object):
    """docstring for cardinfo"""
    tag_id = None
    in_time = None
    out_time = None
    def __init__(self, uid):
        self.tag_id = copy.deepcopy(uid)

    def get_tag_id(self):
        return self.tag_id

    def set_in_time(self, time):
        self.in_time = time
        return self.in_time
        
    def get_in_time(self):
        return self.in_time
        
    def set_out_time(self, time):
        self.out_time = time
        return self.out_time

    def get_out_time(self):
        return self.out_time

class transmitobserver(CardObserver):
    """A card observer that is notified when cards are inserted/removed
    from the system, connects to cards and SELECT DF_TELECOM """

    registeredCards = []
    timeFormat = "%H:%M:%S  %a %d %b"

    def __init__(self):
        self.cards = []

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            if card not in self.cards:
                self.cards += [card]
                # print("+Inserted: ", toHexString(card.atr))
                print("+Inserted card")
                card.connection = card.createConnection()
                card.connection.connect()
                # print("status = %.2x" % (card.connection.connect()))
                uid, sw1, sw2 = card.connection.transmit(
                    APDU_GET_UID)
                # print("%.2x %.2x" % (sw1, sw2))
                # print("response: %s" % (uid))
                if sw1 != 0x90 or sw2 != 0x00:
                    print("Some error. Error code is %.2x %.2x" % (sw1, sw2))
                    return
                isNewCard = True
                for cur_card in self.registeredCards:
                    if cur_card.get_tag_id() == uid:
                        cur_card.set_out_time(datetime.datetime.now())
                        print("=== Card %s:" %(cur_card.get_tag_id()))
                        print("===   In   time: %s" %(cur_card.get_in_time().strftime(self.timeFormat)))
                        print("===   Out  time: %s" %(cur_card.get_out_time().strftime(self.timeFormat)))
                        delta = int((cur_card.get_out_time() - cur_card.get_in_time()).total_seconds()+0.5)
                        print("===   Diff time: %s sec" %(delta))
                        isNewCard = False
                        self.registeredCards.remove(cur_card)
                        break
                if isNewCard:
                    newcard = cardinfo(uid)
                    self.registeredCards += [newcard]
                    newcard.set_in_time(datetime.datetime.now())
                    print("=== Card %s:" %(newcard.get_tag_id()))
                    # print(newcard.get_in_time().__class__.__name__)
                    t = newcard.get_in_time().strftime(self.timeFormat)
                    print("===   In   time: %s" %(t))
                    # print("===   In   time: %s" %(newcard.get_in_time()))


        for card in removedcards:
            # print("-Removed: ", toHexString(card.atr))
            print("-Removed card")
            print()
            if card in self.cards:
                self.cards.remove(card)

if __name__ == '__main__':
    print("Insert or remove a smartcard in the system.")
    print("This program will exit in 100 seconds")
    print("")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)

    sleep(100)