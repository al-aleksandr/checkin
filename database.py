#! /usr/bin/env python
"""
Data base extention for Checkin
"""

from __future__ import print_function
from datetime import datetime
import copy
import os.path
import json
import io
import uuid

from settings import MainDBDir
from logging import log, logd, loge

GlobalCardsDB = { }
# path, mainScriptName = os.path.split(os.path.abspath(os.getcwd()+"/"+sys.argv[0]))
DataBaseFileName = MainDBDir + "/example.json"

def GetNewCard(UID, Type, Name, LastName, State, ExpDate, Info):
    card = {}
    card['UID'] = UID
    card['Type'] = Type
    card['Name'] = Name
    card['LastName'] = LastName
    card['State'] = State
    card['ExpDate'] = ExpDate
    card['Info'] = Info
    return card


def LoadCardsDB(filename):
    global GlobalCardsDB
    if not os.path.isfile(filename):
        return GlobalCardsDB
    return json.load(file(filename))

def GetCardsDB():
    """
    Return Cards Data Base
    """
    global GlobalCardsDB
    if GlobalCardsDB == {}:
        GlobalCardsDB = LoadCardsDB(DataBaseFileName)
    # logd("Count of records in DB: %d" %(len(GlobalCardsDB)))
    return GlobalCardsDB



def UpdateCard(UID, Type, Name, LastName, State, ExpDate, Info):
    """
      Udate Card object in Data Base (CardsDB) and save to file
    """
    CurCard = GetNewCard(UID, Type, Name, LastName, State, ExpDate, Info)
    CardsDB = GetCardsDB()
    if CurCard['UID'] in CardsDB: 
        del CardsDB[CurCard['UID']]
    CardsDB[CurCard['UID']] = CurCard
    filename = DataBaseFileName[:]
    if os.path.isfile(filename):
        os.rename(filename, "tmp/"+str(uuid.uuid4()))
    with open(filename, 'w') as f:
        json.dump(CardsDB, f, indent=4)
    return copy.deepcopy(CardsDB.get(UID, None))

def GetCard(UID):
    """
      Return copy of object Card with UID
    """
    CardsDB = GetCardsDB()
    return  copy.deepcopy(CardsDB.get(UID, None))





def printCardInfo(MyCard):
    if MyCard == None:
        return
    logd("UID       : %s" %(MyCard['UID']))
    logd("Type      : %s" %(MyCard['Type']))
    logd("Name      : %s" %(MyCard['Name']))
    logd("LastName  : %s" %(MyCard['LastName']))
    logd("State     : %s" %(MyCard['State']))
    logd("ExpDate   : %s" %(MyCard['ExpDate']))
    logd("Info      : %s" %(MyCard['Info']))
