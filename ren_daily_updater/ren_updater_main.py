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
import keyring
import pysftp
import time
from os import getenv
from pathlib import Path
import subprocess
import datetime
from dotenv import load_dotenv
from rcmailsend import mail_send #Self Created Module
###########

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
#Function to Call Python Script and Append Log Entry
def pyscript_call(scriptPath,scriptName,logFile):
    #Call a python script
    subprocess.run(["python3", scriptPath + scriptName])
    #Write entry to log
    with open(logFile,'a') as a_writer:
        a_writer.write("---\n")
        a_writer.write("The " + scriptName + " script ran successfully \n")
        a_writer.write("---\n")
#Function to Log Error
def log_script_error(scriptName,logFile):
    #Log Error
    with open(logFile,'a') as a_writer:
        a_writer.write("---\n")
        a_writer.write("The " + scriptName + " failed! \n")
        a_writer.write("---\n")
###########

###Log Begin
with open(logFile,'a') as a_writer:
    a_writer.write("------------------\n")
    a_writer.write("The Renaissance Updater Script was started on " + startTime + "\n")
    a_writer.write("---\n")
###########

###Call the SubScripts
for subScript in scriptList:
    try:
        pyscript_call(scriptPath,subScript,logFile)
    except:
        log_script_error(script,logFile)
###########

###Email Results###
mail_send(logToEmail,logSubject,logFile)
########