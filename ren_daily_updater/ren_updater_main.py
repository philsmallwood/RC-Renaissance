#!/usr/bin/env python3
### Renaissance Update Main Script
### Script to call the various sub-scripts that 
### create create, fix, and upload files for 
### Renaissance Application
### Scripts: 
# ren_student.py
# ren_teacher.py
# ren_sections_enrollments_licensed.py
# ren_sections_enrollments_special.py
# ren_uploader.py

###Import Modules###
import time
import datetime
from os import getenv
from dotenv import load_dotenv
from rcmailsend import mail_send #Self Created Module
#######

###Variables###
#Load .ENV File
load_dotenv()
#Date
CurrentDate = datetime.date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
startTime = time.ctime()
#Scripts
scriptPath = getenv('scriptPath')
scriptList = (
    'ren_student.py', 'ren_teacher.py',
    'ren_sections_enrollments_licensed.py',
    'ren_sections_enrollments_special.py',
    'ren_uploader.py')
#Email Vars
logToEmail = getenv('logToEmail')
logSubject = 'Renaissance Updater Log'
logFile = getenv('logFilePath') + "Renaissance-" + Date + ".log"
##Function Definitions
#Function to call a python script and append info to a log file
def pyscript_call(scriptPath,scriptName,logFile):
    #Call a python script
    os.system("python3 %s" % scriptPath + scriptName)
    #Write entry to log
    f = open(logFile, "a")
    f.write("---\n")
    f.write("The " + scriptName + " script ran successfully \n")
    f.write("---\n")
    f.close()
def log_script_error(scriptName,logFile):
    #Write the Error to the Log
        ###Log Error
    f = open(logFile, "a")
    f.write("---\n")
    f.write("The " + scriptName + " failed! \n")
    f.write("---\n")
    f.close()
###########

###Log Begin
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Renaissance Updater Script was started on " + startTime + "\n")
f.write("---\n")
f.close()


for script in scriptList:
    try:
        pyscript_call(scriptPath,script,logFile)
    except:
        log_script_error(script,logFile)



###Email Results###
mail_send(logToEmail,logSubject,logFile)
########