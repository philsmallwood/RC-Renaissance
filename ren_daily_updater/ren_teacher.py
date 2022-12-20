#!/usr/bin/env python3
###Renaissance Student File Script
###Script to create a file with student info
###to upload to Renaissance
###Requires exported user file from Classlink

###Import Modules###
import pandas as pd
from zipfile import ZipFile
from os import getenv
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#######

###Variables###
#Load Env File
load_dotenv()
#Output File
localUpFilePath = getenv('TeacherUploadFile')
#Data Files
classlinkPath = getenv('ClasslinkExportPath')
classlinkZip = getenv('classlinkZipFile')
classlinkUserFile = getenv('classlinkUserFile')
classlinkUserFileExtracted = getenv('classlinkUserFileExtracted')
#Schools with Ren Licenses
LicensedSchools = getenv('LicensedSchools').split(",")
#Google Variables
googleAppScope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
googleOAuth = getenv('oauthPath') + getenv('oauthKey')
googleCredentials = ServiceAccountCredentials.from_json_keyfile_name(googleOAuth, googleAppScope)
specEdSheetName = getenv('sheetName')
########
#Empty DataFrames
df_specEdCheck = pd.DataFrame()
df_tempStudentInfo = pd.DataFrame()
df_licensedSchools = pd.DataFrame()
df_final = pd.DataFrame()
#######

###Classlink Data###
#Extract User File from Classlink Export
with ZipFile(classlinkZip, 'r') as zip:
    zip.extract(classlinkUserFile,classlinkPath)
#Read User File into a Dataframe
df_userFile = pd.read_csv(classlinkUserFileExtracted, dtype=str, \
    skiprows = 1, header=None)
#Keep only the Teachers
df_teachers = df_userFile.loc[(df_userFile[5] == 'teacher') | (df_userFile[5] == 'aide')]
#Drop 'fake' accounts
df_teachers = df_teachers[~df_teachers[12].str.contains("test")]
########

###Format Temp Dataframe###
df_tempStudentInfo['TID'] = df_teachers[0]
df_tempStudentInfo['TSTATEID'] = ''
df_tempStudentInfo['TFIRST'] = df_teachers[8].str.lower()
df_tempStudentInfo['SMIDDLE'] = df_teachers[10]
df_tempStudentInfo['TLAST'] = df_teachers[9].str.lower()
df_tempStudentInfo['TGENDER'] = ''
df_tempStudentInfo['TPOSITION'] = ''
df_tempStudentInfo['TUSERNAME'] = df_teachers[12]
df_tempStudentInfo['PASSWORD'] = getenv('FakePassword')
df_tempStudentInfo['school_id'] = df_teachers[4]
########

###Get Data from Google Sheet###
##Connect to Google
gClient = gspread.authorize(googleCredentials)
#sheet = gClient.open('Contractor_Access_File')
##Open the Sheet and Get Data
specEdSheet = gClient.open(specEdSheetName)
specEdRecords = specEdSheet.sheet1.get_all_records()
##Load Data into Dataframe
df_specEdTeachers = pd.DataFrame.from_dict(specEdRecords)
##Get Needed Parts for Checking
df_specEdCheck['TFIRST'] = df_specEdTeachers['First Name'].str.lower()
df_specEdCheck['TLAST'] = df_specEdTeachers['Last Name'].str.lower()
########

###Create Spec ED Teacher DataFrame###
df_specEd = pd.merge(df_tempStudentInfo,df_specEdCheck, how='inner')
########

###Create Licensed School Teacher DataFrame###
for School in LicensedSchools:
    df = df_tempStudentInfo.loc[(df_tempStudentInfo['school_id'] == '320' + School)]
    df_licensedSchools = pd.concat([df,df_licensedSchools])
########

###Format Final DataFrame###
df_final = pd.concat([df_specEd,df_licensedSchools])
########
    
###Export Final File###
df_final.to_csv(localUpFilePath, index=False)
########

							