#! /usr/bin/env python
"""
Log analizer for Checkin

Name LastName, Date, EnterTime, ExitTime, DiffTime
"""

import os
import datetime

LOG_MAIN_DIR = "./checkin/log"
timeFormat = "%H:%M:%S  %a %d %b"


testRecordAdmin = [
    "14:45:47 : GetTypeOfCard. uid: 71 46 BB DE 0A 4F 0C A0 00 00",
    "14:45:47 : ProcessEmployeeCard. Enter: 71 46 BB DE 0A 4F 0C A0 00 00",
    "14:45:47 : New card: 71 46 BB DE 0A 4F 0C A0 00 00",
    "14:45:47 : Enter time: 14:45:47  Fri 02 Sep",
    "14:45:47 : ",
    "14:45:47 : Enter. Employee:",
    "14:45:47 :                 Name : A",
    "14:45:47 :             LastName : S",
    "14:45:47 :                 Info : Administrator",
    "14:45:47 :             Card num : 71 46 BB DE 0A 4F 0C A0 00 00",
    "14:45:47 :                 Type : Employee",
    "14:45:47 :                State : Active",
    "14:45:47 :              ExpDate : 31/12/20 10:30",
    "14:45:47 :            EnterTime : 14:45:47  Fri 02 Sep",
    "14:45:47 : ------------------------------------------------------",
    ]

testRecordVisitor = [
    "11:54:41 : GetTypeOfCard. uid: 1D 0E FB 2E 0A 4F 0C A0 00 00",
    "11:54:41 : ProcessVisitorCard. Enter: 1D 0E FB 2E 0A 4F 0C A0 00 00",
    "11:54:41 : Card 1D 0E FB 2E 0A 4F 0C A0 00 00:",
    "11:54:41 :   Enter time: 09:57:46  Fri 02 Sep",
    "11:54:41 :   Exit  time: 11:54:41  Fri 02 Sep",
    "11:54:41 :   Diff  time: 7015 sec",
    "11:54:41 :   Price     : 63 uah",
    "11:54:41 : ",
    "11:54:41 : Exit. Visitor:",
    "11:54:41 :                 Name : Common card #108",
    "11:54:41 :             LastName : -",
    "11:54:41 :                 Info : Common space card",
    "11:54:41 :             Card num : 1D 0E FB 2E 0A 4F 0C A0 00 00",
    "11:54:41 :                 Type : Visitor",
    "11:54:41 :                State : Active",
    "11:54:41 :              ExpDate : 31/12/20 10:30",
    "11:54:41 :            EnterTime : 09:57:46  Fri 02 Sep",
    "11:54:41 :             ExitTime : 11:54:41  Fri 02 Sep",
    "11:54:41 :       DiffTime(H:MM) : 1:56",
    "11:54:41 :           Price(UAH) : 63",
    "11:54:41 : ------------------------------------------------------",
    ]

def get_card_info_from_record(record):
    card = {}
    for line in record:
        splitLine = line[11:].split(' : ')
        if 'Enter. ' in splitLine[0]:
            card['EnterExit'] = 'Enter'
            continue
        if 'Exit. ' in splitLine[0]:
            card['EnterExit'] = 'Exit'
            continue
        if len(splitLine) < 2:
            continue
        card[splitLine[0].strip()] = splitLine[1]
    if card.get('EnterTime', None):
        card['EnterTime'] = datetime.datetime.strptime(card['EnterTime'], timeFormat)
        card['EnterTime'] = card['EnterTime'].replace(year=2016)
    if card.get('ExitTime', None):
        card['ExitTime'] = datetime.datetime.strptime(card['ExitTime'], timeFormat)
        card['ExitTime'] = card['ExitTime'].replace(year=2016)
    return card

def analize_file(fileName):
    curYear = 2000 + int(fileName[-17:-15])
    cardsFromFile = []
    card = {}
    prevLines = []
    with open(fileName) as f:
        for line in f:
            if line in prevLines:
                continue
            prevLines.append(line)
            splitLine = line[11:].rstrip('\n').split(' : ')
            # print(splitLine)
            if '------------------------------------------------------' in splitLine[0]:
                # TODO: Do not skip sale info
                if card.get('Type', None):
                    if card['Type'] == 'Employee':
                        cardsFromFile.append(card)
                # print card
                # print
                card = {}
                continue
            if 'Sale' in splitLine[0]:
                card = {}
                card['EnterExit'] = 'Enter'
                card['Type'] = 'Sale'
                continue
            if 'Enter. ' in splitLine[0]:
                card = {}
                card['EnterExit'] = 'Enter'
                continue
            if 'Exit. ' in splitLine[0]:
                card = {}
                card['EnterExit'] = 'Exit'
                continue
            if len(splitLine) < 2:
                continue
            card[splitLine[0].strip()] = splitLine[1]
            if splitLine[0].strip() == 'EnterTime':
                card['EnterTime'] = datetime.datetime.strptime(card['EnterTime'], timeFormat)
                card['EnterTime'] = card['EnterTime'].replace(year=curYear)
            if splitLine[0].strip() == 'ExitTime':
                card['ExitTime'] = datetime.datetime.strptime(card['ExitTime'], timeFormat)
                card['ExitTime'] = card['ExitTime'].replace(year=curYear)
    return cardsFromFile


def analize_logs(LogDir):
    for fileName in os.listdir(LogDir):
        if fileName.endswith(".log"):
            fullName = LogDir+'/'+fileName
            print("Analizing: %s" % fullName)
            cardsFromFile = analize_file(fullName)
            print("Found %d cards" % len(cardsFromFile))
            create_csv_file(cardsFromFile, LogDir+'/output.csv')

def save_card_to_file(card, fileName):
    with open(fileName, "a") as f:
        # print
        # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print card
        # print
        f.write("%s,%s,%s,%s,%s\n" %(
            card['Type'],
            card['EnterExit'],
            card['Name']+' '+card['LastName'],
            card.get('EnterTime', ""),
            card.get('ExitTime', ""),
            )
        )


def create_csv_file(cardsFromFile, fileName):
    for card in cardsFromFile:
        save_card_to_file(card, fileName)

def get_employee_work_time(LogDir):
    with open(LogDir+'/output.csv', "w") as f:
        pass
    analize_logs(LOG_MAIN_DIR)

if __name__ == '__main__':
    print
    print
    analize_logs(LOG_MAIN_DIR)
    # cardsFromFile = analize_file(LOG_MAIN_DIR+'/16-09-02_full.log')
    # cardsFromFile = analize_file(LOG_MAIN_DIR+'/16-07-16_full.log')
    # create_csv_file(cardsFromFile, LOG_MAIN_DIR+'/output.csv')
    # print get_card_info_from_record(testRecordAdmin)
    # get_employee_work_time(LOG_MAIN_DIR)
    print
    print
    # print get_card_info_from_record(testRecordVisitor)
