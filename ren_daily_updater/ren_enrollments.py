#!/usr/bin/env python3
###Renaissance Enrollments File Script
###Script to create a file with student
###class enrollment info to upload 
###to Renaissance
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
localUpFilePath = getenv('EnrollmentUploadFile')
#Data Files
classlinkPath = getenv('ClasslinkExportPath')
classlinkZip = getenv('classlinkZipFile')
classlinkEnrollmentsFile = getenv('classlinkEnrollmentsFile')
classlinkEnrollmentsFileExtracted = getenv('classlinkEnrollmentsFileExtracted')
#Schools with Ren Licenses
LicensedSchools = getenv('LicensedSchools').split(",")
#Empty DataFrames
df_final = pd.DataFrame()
#######

###Classlink Data###
#Extract User File from Classlink Export
with ZipFile(classlinkZip, 'r') as zip:
    zip.extract(classlinkEnrollmentsFile,classlinkPath)
#Read User File into a Dataframe
df_studentenrollments = pd.read_csv(classlinkEnrollmentsFileExtracted, dtype=str, \
    skiprows = 1, header=None)
#Keep only the Student enrollments
df_studentenrollments = df_studentenrollments.loc[(df_studentenrollments[6] == 'student')]
########

###Format Dataframe###
df_final['School_id'] = df_studentenrollments[4]
df_final['Section_id'] = df_studentenrollments[3]
df_final['Student_id'] = df_studentenrollments[5]
#Cleanup Section ID
df_final['Section_id'] = df_final['Section_id'].str.split("-").str[0]
df_final['Section_id'] = df_final['Section_id'].str.split("_").str[1]
#Drop Uneeded Enrollments
df_final = df_final[df_final['Section_id'].str.contains("1000")]
df_final = df_final[df_final['School_id'].str.contains(LicensedSchools[0]) | \
        df_final['School_id'].str.contains(LicensedSchools[1]) ]
########