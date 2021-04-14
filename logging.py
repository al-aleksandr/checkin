"""
Logging for Checkin
"""

import sys
import os.path
import datetime

from settings import MainLogDir, FullLogFileName, DEBUG_MODE, DATE_FILENAME_FORMAT, TIME_FORMAT
# from checkin import getMainScriptPath

CurrentFullLogFileName = ""

def CreateLogFileByDate(folder, fileNameBase):
    """
      Create file for logging.
      File name format: <date>_<fileNameBase>.log
    """
    curDate = datetime.datetime.now()
    date = curDate.strftime(DATE_FILENAME_FORMAT)
    fname = folder + "/" + date + "_" + fileNameBase + ".log"
    if os.path.isfile(fname):
        return fname
    f = open(fname, 'w+')
    time = curDate.strftime(TIME_FORMAT)
    f.write("File is created at %s %s\n" %(date, time))
    f.close()
    return fname

def CreateLogFiles():
    global CurrentFullLogFileName
    CurrentFullLogFileName = CreateLogFileByDate(MainLogDir, FullLogFileName)

def saveLineToFile(fileName, line):
    if not os.path.isfile(fileName):
        return
    # f = open(fileName, 'w')
    curDate = datetime.datetime.now()
    time = curDate.strftime(TIME_FORMAT)
    with open(fileName, "a") as f:
        f.write("%s : %s\n" %(time, line))
    # f.close()

def printResFormat(text, val, printOnScreen):  # Log common
    """
    text - Description of value (val)
    val  - Value
    printOnScreen - if true then print text on screen
    """
    if text == None or val == None:
        return
    line = "%20s : %s" %(text, val)
    saveLineToFile(CurrentFullLogFileName, line)
    if printOnScreen:
        print(line)

def log(text):  # Log common
    if text == None:
        return
    saveLineToFile(CurrentFullLogFileName, text)
    print(text)

def loge(text): # Log ERROR
    if text == None:
        return
    saveLineToFile(CurrentFullLogFileName, text)
    print(text)

def logd(text): # Log DEBUG
    if text == None:
        return
    saveLineToFile(CurrentFullLogFileName, text)
    if DEBUG_MODE == "YES":
        print(text)
