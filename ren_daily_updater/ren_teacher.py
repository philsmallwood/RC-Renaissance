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
#Empty DataFrames
df_final = pd.DataFrame()
#######

###Classlink Data###
#Extract User File from Classlink Export
with ZipFile(classlinkZip, 'r') as zip:
    zip.extract(classlinkUserFile,classlinkPath)
#Read User File into a Dataframe
df_userFile = pd.read_csv(classlinkUserFileExtracted, dtype=str)
#Keep only the Admin, Teacher, and Student users for comparison later
#All the rest will have been added by previous run of this script
df_teachers = df_userFile.loc[(df_userFile['role'] == 'teacher')]
########

###Format Dataframe###
df_final['TID'] = df_teachers[0]
df_final['TSTATEID'] = ''
df_final['TFIRST'] = df_teachers[8]
df_final['SMIDDLE'] = df_teachers[10]
df_final['TLAST'] = df_teachers[9]
df_final['TGENDER'] = ''
df_final['TPOSITION'] = ''
df_final['TUSERNAME'] = df_teachers[6]
df_final['PASSWORD'] = getenv('FakePassword')
########

###Export Final File###
df_final.to_csv(localUpFilePath, index=False)
########

							