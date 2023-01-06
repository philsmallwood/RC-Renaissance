#!/usr/bin/env python3
### Renaissance File Uploader
### Script to upload files the newest to
### Titan Nutrition Management System
### Requires time, pandas, keyring, datetime,
###pysftp
###For keyring, need to set the username/password for sftp sites for downloads and uploads


###Import Modules###
import pysftp
import keyring
from os import getenv
from dotenv import load_dotenv
#######


###Variables###
#Load .ENV File
load_dotenv()
#Renaissance SFTP Vars
renaissanceHostname = getenv('renaissanceHostname')
renaissanceUsername = getenv('renaissanceUsername')
renaissanceServiceName = getenv('renaissanceServiceName')
#Files
uploadFiles = [getenv('StudentUploadFile'),
    getenv('TeacherUploadFile'),
    getenv('LicensedSectionUploadFile'),
    getenv('LicensedEnrollmentUploadFile')]
#######

###Upload Files to Classlink###
with pysftp.Connection(host=titanHostname, username=renaissanceUsername, \
    password=keyring.get_password(renaissanceServiceName, renaissanceUsername)) as sftp:
    for upFile in uploadFiles:
        sftp.put(upFile,upFile.split('/')[-1])
#######