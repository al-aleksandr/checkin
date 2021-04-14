"""
Setting file for Checkin
"""

import sys
import os.path
import datetime

TIME_FORMAT = "%H:%M:%S"

DATE_FILENAME_FORMAT = "%y-%m-%d"
DEBUG_MODE = "NO"
mainScriptPath, mainScriptName = os.path.split(os.path.abspath(os.getcwd()+"/"+sys.argv[0]))

MainLogDir = mainScriptPath + "/log"
MainDBDir = mainScriptPath + "/db_sample"

FullLogFileName = "full"

# MultiplyTimeForDebug = 1 for work mode and any for other for debug
MultiplyTimeForDebug = 1
# MultiplyTimeForDebug = 60

def getMainScriptPath():
    return mainScriptPath
