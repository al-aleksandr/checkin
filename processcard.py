"""
Process cards for Checkin
"""
import copy
import datetime
import os
import json
import uuid

import database
from logging import log, logd, loge, printResFormat
from price import getPrice, getSalePrice
from settings import MainLogDir, MultiplyTimeForDebug

ListofCheckinFileName = MainLogDir + "/ListofCheckin.json"
timeFormat = "%H:%M:%S  %a %d %b"
CardTypeEmployee    = "Employee"
CardTypeCoworker    = "Coworker"
CardTypeVisitor     = "Visitor"
CardTypeSale        = "Sale"
CardTypeUnknown     = "Unknown"

ListofCheckin = {}  # ListofCheckin { newCard, newCard, ...., newCard }; newCard { 'uid' : 'time' } - time when card was detected

def saveListofCheckin(filename):
    if os.path.isfile(filename):
        os.rename(filename, "tmp/ListofCheckin_"+str(uuid.uuid4()))
    with open(filename, 'w') as f:
        # json.dump(ListofCheckin, f, indent=4)
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else obj
        response = json.dump(ListofCheckin, f, indent=4, default=dthandler)


def loadListofCheckin(filename):
    global ListofCheckin
    if not os.path.isfile(filename):
        return ListofCheckin
    try:
        ListofCheckin = json.load(file(filename))
    except ValueError, e:
        os.rename(filename, "tmp/ListofCheckin_bad_"+str(uuid.uuid4()))

    Today = datetime.date.today()

    for key in ListofCheckin.copy():
        ReadDate = datetime.datetime.strptime(ListofCheckin[key], '%Y-%m-%dT%H:%M:%S.%f')
        ListofCheckin[key] = ReadDate
        if ReadDate.date() < Today:
            UpdatedTime = datetime.datetime.combine(ReadDate.date(), datetime.time(22, 0, 0, 0)) 
            newCard = {}
            newCard[key] = UpdatedTime
            PrintProcessCardResult(processNewCard(newCard))

    return ListofCheckin

def processNewCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected

      retCardInfo['UID']
      retCardInfo['Type']
      retCardInfo['Name']
      retCardInfo['LastName']
      retCardInfo['State']
      retCardInfo['ExpDate']
      retCardInfo['Info']
      retCardInfo['EnterTime']
      retCardInfo['ExitTime']
      retCardInfo['DiffTime']
      retCardInfo['Price']
      retCardInfo['EnterExit']  - Enter or exit
    """
    cardType = GetTypeOfCard(newCard.keys()[0])

    if cardType == CardTypeVisitor:
        retCardInfo = ProcessVisitorCard(newCard)
    elif cardType == CardTypeCoworker:
        retCardInfo = ProcessCoworkerCard(newCard)
    elif cardType == CardTypeEmployee:
        retCardInfo = ProcessEmployeeCard(newCard)
    elif cardType == CardTypeSale:
        retCardInfo = ProcessSaleCard(newCard)
    else:
        retCardInfo = ProcessUnknownCard(newCard)

    saveListofCheckin(ListofCheckinFileName)
    return retCardInfo

def GetTypeOfCard(uid):
    logd("GetTypeOfCard. uid: %s" %uid)
    curCard = database.GetCard(uid)
    if curCard != None:
        return curCard['Type']
    else:
        return CardTypeUnknown
    

def ProcessCoworkerCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected
      ListofCheckin  [ newCard, newCard, ...., newCard ]
    """
    global ListofCheckin

    logd("ProcessCoworkerCard. Enter: %s" %(newCard.keys()[0]))

    uid = newCard.keys()[0]
    curCard = database.GetCard(uid)
    retCardInfo = {}
    retCardInfo['UID']       = curCard['UID']
    retCardInfo['Type']      = curCard['Type']
    retCardInfo['Name']      = curCard['Name']
    retCardInfo['LastName']  = curCard['LastName']
    retCardInfo['State']     = curCard['State']
    retCardInfo['ExpDate']   = curCard['ExpDate']
    retCardInfo['Info']      = curCard['Info']
    retCardInfo['EnterTime'] = None
    retCardInfo['ExitTime']  = None
    retCardInfo['DiffTime']  = None
    retCardInfo['Price']     = None
    retCardInfo['EnterExit'] = "Unknown"
    if uid in ListofCheckin:
        retCardInfo['EnterExit'] = "Exit"
        enterTime = ListofCheckin[uid]
        exitTime  = newCard[uid]
        delta = int((exitTime - enterTime).total_seconds()+0.5)*MultiplyTimeForDebug
        retCardInfo['EnterTime'] = enterTime.strftime(timeFormat)
        retCardInfo['ExitTime']  = exitTime.strftime(timeFormat)
        retCardInfo['DiffTime']  = delta
        logd("Card %s:" % (uid))
        logd("  Enter time: %s" % (retCardInfo['EnterTime']))
        logd("  Exit  time: %s" % (retCardInfo['ExitTime']))
        logd("  Diff  time: %s sec" %(retCardInfo['DiffTime']))
        del ListofCheckin[uid]
    else:
        retCardInfo['EnterExit'] = "Enter"
        ListofCheckin.update(newCard)
        retCardInfo['EnterTime'] = ListofCheckin[uid].strftime(timeFormat)
        logd("New card: %s" % (uid))
        logd("Enter time: %s" % (retCardInfo['EnterTime']))
    logd("")
    return retCardInfo

def ProcessEmployeeCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected
      ListofCheckin  [ newCard, newCard, ...., newCard ]
    """
    global ListofCheckin

    logd("ProcessEmployeeCard. Enter: %s" %(newCard.keys()[0]))

    uid = newCard.keys()[0]
    curCard = database.GetCard(uid)
    retCardInfo = {}
    retCardInfo['UID']       = curCard['UID']
    retCardInfo['Type']      = curCard['Type']
    retCardInfo['Name']      = curCard['Name']
    retCardInfo['LastName']  = curCard['LastName']
    retCardInfo['State']     = curCard['State']
    retCardInfo['ExpDate']   = curCard['ExpDate']
    retCardInfo['Info']      = curCard['Info']
    retCardInfo['EnterTime'] = None
    retCardInfo['ExitTime']  = None
    retCardInfo['DiffTime']  = None
    retCardInfo['Price']     = None
    retCardInfo['EnterExit'] = "Unknown"
    if uid in ListofCheckin:
        retCardInfo['EnterExit'] = "Exit"
        enterTime = ListofCheckin[uid]
        exitTime  = newCard[uid]
        delta = int((exitTime - enterTime).total_seconds()+0.5)*MultiplyTimeForDebug
        retCardInfo['EnterTime'] = enterTime.strftime(timeFormat)
        retCardInfo['ExitTime']  = exitTime.strftime(timeFormat)
        retCardInfo['DiffTime']  = delta
        logd("Card %s:" % (uid))
        logd("  Enter time: %s" % (retCardInfo['EnterTime']))
        logd("  Exit  time: %s" % (retCardInfo['ExitTime']))
        logd("  Diff  time: %s sec" %(retCardInfo['DiffTime']))
        del ListofCheckin[uid]
    else:
        retCardInfo['EnterExit'] = "Enter"
        ListofCheckin.update(newCard)
        retCardInfo['EnterTime'] = ListofCheckin[uid].strftime(timeFormat)
        logd("New card: %s" % (uid))
        logd("Enter time: %s" % (retCardInfo['EnterTime']))
    logd("")
    return retCardInfo

def ProcessVisitorCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected
      ListofCheckin  [ newCard, newCard, ...., newCard ]
    """
    global ListofCheckin

    logd("ProcessVisitorCard. Enter: %s" %(newCard.keys()[0]))

    uid = newCard.keys()[0]
    curCard = database.GetCard(uid)
    retCardInfo = {}
    retCardInfo['UID']       = curCard['UID']
    retCardInfo['Type']      = curCard['Type']
    retCardInfo['Name']      = curCard['Name']
    retCardInfo['LastName']  = curCard['LastName']
    retCardInfo['State']     = curCard['State']
    retCardInfo['ExpDate']   = curCard['ExpDate']
    retCardInfo['Info']      = curCard['Info']
    retCardInfo['EnterTime'] = None
    retCardInfo['ExitTime']  = None
    retCardInfo['DiffTime']  = None
    retCardInfo['Price']     = None
    retCardInfo['EnterExit'] = "Unknown"
    if uid in ListofCheckin:
        retCardInfo['EnterExit'] = "Exit"
        enterTime = ListofCheckin[uid]
        exitTime  = newCard[uid]
        delta = int((exitTime - enterTime).total_seconds()+0.5)*MultiplyTimeForDebug
        price = getPrice(delta)
        retCardInfo['EnterTime'] = enterTime.strftime(timeFormat)
        retCardInfo['ExitTime']  = exitTime.strftime(timeFormat)
        retCardInfo['DiffTime']  = delta
        retCardInfo['Price']     = price
        logd("Card %s:" % (uid))
        logd("  Enter time: %s" % (retCardInfo['EnterTime']))
        logd("  Exit  time: %s" % (retCardInfo['ExitTime']))
        logd("  Diff  time: %s sec" %(retCardInfo['DiffTime']))
        logd("  Price     : %s uah" %(retCardInfo['Price']))
        del ListofCheckin[uid]
    else:
        retCardInfo['EnterExit'] = "Enter"
        ListofCheckin.update(newCard)
        retCardInfo['EnterTime'] = ListofCheckin[uid].strftime(timeFormat)
        logd("New card: %s" % (uid))
        logd("Enter time: %s" % (retCardInfo['EnterTime']))
    logd("")
    return retCardInfo

def ProcessSaleCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected
      ListofCheckin  [ newCard, newCard, ...., newCard ]
    """
    logd("ProcessSaleCard. Time: %s" %(newCard.values()[0]))

    uid = newCard.keys()[0]
    time = newCard.values()[0]
    curCard = database.GetCard(uid)
    retCardInfo = {}
    retCardInfo['UID']       = curCard['UID']
    retCardInfo['Type']      = curCard['Type']
    retCardInfo['Name']      = curCard['Name']
    retCardInfo['LastName']  = curCard['LastName']
    retCardInfo['State']     = curCard['State']
    retCardInfo['ExpDate']   = curCard['ExpDate']
    retCardInfo['Info']      = curCard['Info']
    retCardInfo['EnterTime'] = None
    retCardInfo['ExitTime']  = None
    retCardInfo['DiffTime']  = None
    retCardInfo['Price']     = getSalePrice(retCardInfo['Name'])
    retCardInfo['EnterExit'] = None
    retCardInfo['EnterTime'] = time.strftime(timeFormat)
    retCardInfo['ExitTime']  = time.strftime(timeFormat)
    retCardInfo['DiffTime']  = 0
    logd("Card %s:" % (uid))
    logd("  Enter time: %s" % (retCardInfo['EnterTime']))
    logd("  Exit  time: %s" % (retCardInfo['ExitTime']))
    logd("  Diff  time: %s sec" %(retCardInfo['DiffTime']))
    logd("")
    return retCardInfo

def ProcessUnknownCard(newCard):
    """
      newCard        { 'uid' : 'time' } - time when card was detected
      ListofCheckin  [ newCard, newCard, ...., newCard ]
    """
    retCardInfo = {}
    retCardInfo['UID']  = newCard.keys()[0]
    retCardInfo['Type'] = CardTypeUnknown
    return retCardInfo

def PrintByKey(curDict, key):
    val = curDict.get(key, None)
    if val:
        log("")
    curDict

def PrintProcessCoworkerCard(retCardInfo):
    if retCardInfo == None:
        logd("PrintProcessCardResult. No card info")
        return
    log("%s. %s:" %(retCardInfo['EnterExit'], retCardInfo.get('Type', None)))
    printResFormat("  ExpDate", retCardInfo.get('ExpDate', None), True)
    printResFormat("  Name", retCardInfo.get('Name', None), True)
    printResFormat("  LastName", retCardInfo.get('LastName', None), True)
    printResFormat("  Info", retCardInfo.get('Info', None), True)
    printResFormat("  Card num", retCardInfo.get('UID', None), True)
    printResFormat("  Type", retCardInfo.get('Type', None), False)
    printResFormat("  State", retCardInfo.get('State', None), False)
    printResFormat("  EnterTime", retCardInfo.get('EnterTime', None), True)
    printResFormat("  ExitTime", retCardInfo.get('ExitTime', None), True)
    secCount = retCardInfo.get('DiffTime', None)
    if secCount:
        m, s = divmod(secCount, 60)
        h, m = divmod(m, 60)
        strTimeDelta = "%d:%02d" % (h, m)
        printResFormat("  DiffTime(H:MM)", strTimeDelta, True)
    printResFormat("  Price(UAH)", retCardInfo.get('Price', None), False)

def PrintProcessEmployeeCard(retCardInfo):
    if retCardInfo == None:
        logd("PrintProcessCardResult. No card info")
        return
    log("%s. %s:" %(retCardInfo['EnterExit'], retCardInfo.get('Type', None)))
    printResFormat("  ExpDate", retCardInfo.get('ExpDate', None), False)
    printResFormat("  Name", retCardInfo.get('Name', None), True)
    printResFormat("  LastName", retCardInfo.get('LastName', None), True)
    printResFormat("  Info", retCardInfo.get('Info', None), True)
    printResFormat("  Card num", retCardInfo.get('UID', None), True)
    printResFormat("  Type", retCardInfo.get('Type', None), False)
    printResFormat("  State", retCardInfo.get('State', None), False)
    printResFormat("  EnterTime", retCardInfo.get('EnterTime', None), True)
    printResFormat("  ExitTime", retCardInfo.get('ExitTime', None), True)
    secCount = retCardInfo.get('DiffTime', None)
    if secCount:
        m, s = divmod(secCount, 60)
        h, m = divmod(m, 60)
        strTimeDelta = "%d:%02d" % (h, m)
        printResFormat("  DiffTime(H:MM)", strTimeDelta, True)

def PrintProcessVisitorCard(retCardInfo):
    if retCardInfo == None:
        logd("PrintProcessCardResult. No card info")
        return
    log("%s. %s:" %(retCardInfo['EnterExit'], retCardInfo.get('Type', None)))
    printResFormat("  ExpDate", retCardInfo.get('ExpDate', None), False)
    printResFormat("  Name", retCardInfo.get('Name', None), True)
    printResFormat("  LastName", retCardInfo.get('LastName', None), False)
    printResFormat("  Info", retCardInfo.get('Info', None), False)
    printResFormat("  Card num", retCardInfo.get('UID', None), True)
    printResFormat("  Type", retCardInfo.get('Type', None), False)
    printResFormat("  State", retCardInfo.get('State', None), False)
    printResFormat("  EnterTime", retCardInfo.get('EnterTime', None), True)
    printResFormat("  ExitTime", retCardInfo.get('ExitTime', None), True)
    secCount = retCardInfo.get('DiffTime', None)
    if secCount:
        m, s = divmod(secCount, 60)
        h, m = divmod(m, 60)
        strTimeDelta = "%d:%02d" % (h, m)
        printResFormat("  DiffTime(H:MM)", strTimeDelta, True)
    printResFormat("  Price(UAH)", retCardInfo.get('Price', None), True)

def PrintProcessSaleCard(retCardInfo):
    if retCardInfo == None:
        logd("PrintProcessCardResult. No card info")
        return
    log("%s:" %(retCardInfo.get('Type', "Unknown card type")))
    printResFormat("  ExpDate", retCardInfo.get('ExpDate', None), False)
    printResFormat("  Name", retCardInfo.get('Name', None), True)
    printResFormat("  LastName", retCardInfo.get('LastName', None), False)
    printResFormat("  Info", retCardInfo.get('Info', None), False)
    printResFormat("  Card num", retCardInfo.get('UID', None), False)
    printResFormat("  Type", retCardInfo.get('Type', None), False)
    printResFormat("  State", retCardInfo.get('State', None), False)
    printResFormat("  Time", retCardInfo.get('EnterTime', None), True)
    printResFormat("  Price(UAH)", retCardInfo.get('Price', None), True)

def PrintProcessUnknownCard(retCardInfo):
    log("Unknown card type. uid: %s" %(retCardInfo['UID']))

def PrintProcessCardResult(retCardInfo):
    """
      retCardInfo['UID']
      retCardInfo['Type']
      retCardInfo['Name']
      retCardInfo['LastName']
      retCardInfo['State']
      retCardInfo['ExpDate']
      retCardInfo['Info']
      retCardInfo['EnterTime']
      retCardInfo['ExitTime']
      retCardInfo['DiffTime']
      retCardInfo['Price']
      retCardInfo['EnterExit']  - Enter or exit
    """
    cardType = retCardInfo.get('Type', None)

    if cardType == CardTypeVisitor:
        retCardInfo = PrintProcessVisitorCard(retCardInfo)
    elif cardType == CardTypeCoworker:
        retCardInfo = PrintProcessCoworkerCard(retCardInfo)
    elif cardType == CardTypeEmployee:
        retCardInfo = PrintProcessEmployeeCard(retCardInfo)
    elif cardType == CardTypeSale:
        retCardInfo = PrintProcessSaleCard(retCardInfo)
    else:
        retCardInfo = PrintProcessUnknownCard(retCardInfo)


    # if retCardInfo == None:
    #     logd("PrintProcessCardResult. No card info")
    #     return
    # log("%s" %(retCardInfo['EnterExit']))
    # printResFormat("Card num", retCardInfo.get('UID', None), True)
    # printResFormat("  Type", retCardInfo.get('Type', None), True)
    # printResFormat("  Name", retCardInfo.get('Name', None), True)
    # printResFormat("  LastName", retCardInfo.get('LastName', None), True)
    # printResFormat("  State", retCardInfo.get('State', None), True)
    # printResFormat("  ExpDate", retCardInfo.get('ExpDate', None), True)
    # printResFormat("  Info", retCardInfo.get('Info', None), True)
    # printResFormat("  EnterTime", retCardInfo.get('EnterTime', None), True)
    # printResFormat("  ExitTime", retCardInfo.get('ExitTime', None), True)
    # secCount = retCardInfo.get('DiffTime', None)
    # if secCount:
    #     m, s = divmod(secCount, 60)
    #     h, m = divmod(m, 60)
    #     strTimeDelta = "%d:%02d" % (h, m)
    #     printResFormat("  DiffTime", strTimeDelta, True)
    # printResFormat("  Price", retCardInfo.get('Price', None), True)
