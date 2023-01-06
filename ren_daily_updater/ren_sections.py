#!/usr/bin/env python3
###Renaissance Section & Enrollments File Script
###Script to create two files with section and 
###enrollment info to upload to Renaissance
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
localUpFilePath = getenv('SectionUploadFile')
#Data Files
classlinkPath = getenv('ClasslinkExportPath')
classlinkZip = getenv('classlinkZipFile')
classlinkSectionFile = getenv('classlinkSectionFile')
classlinkSectionFileExtracted = getenv('classlinkSectionFileExtracted')
classlinkEnrollmentFile = getenv('classlinkEnrollmentsFile')
classlinkEnrollmentFileExtracted = getenv('classlinkEnrollmentsFileExtracted')
classlinkStudentFile = getenv('StudentUploadFile')
classlinkTeacherFile = getenv('TeacherUploadFile')
#Schools with Ren Licenses
LicensedSchools = getenv('LicensedSchools').split(",")
#Teacher File Columns
colTeacherFile = { 0 : 'TID',
    2 : 'TFirst',
    4 : 'TLast'}
#Empty DataFrames
df_licensedSchoolSections = pd.DataFrame()
df_licensedSchoolEnrollments = pd.DataFrame()
df_licensedSchoolSectionsFinal = pd.DataFrame()




###Classlink Data###
#Extract Section and Enrollment Files from Classlink Export
with ZipFile(classlinkZip, 'r') as zip:
    zip.extract(classlinkSectionFile,classlinkPath)
    zip.extract(classlinkEnrollmentFile,classlinkPath)
#Read Section and Enrollment Files into a Dataframe
df_sectionFile = pd.read_csv(classlinkSectionFileExtracted, dtype=str, \
    skiprows = 1, header=None)
df_enrollmentFile = pd.read_csv(classlinkEnrollmentFileExtracted, dtype=str, \
    skiprows = 1, header=None)
df_studentFile = pd.read_csv(classlinkStudentFile, dtype=str, \
    skiprows = 1, header=None)
df_teacherFile = pd.read_csv(classlinkTeacherFile, dtype=str, \
    skiprows = 1, header=None)
df_teacherFile.rename(columns=colTeacherFile, inplace=True)
########

###Licensed Schools###
#Create Licensed School Section Dataframe
for School in LicensedSchools:
    df = df_sectionFile[df_sectionFile[9] == '320' + School]
    df_licensedSchoolSections = pd.concat([df,df_licensedSchoolSections])
#Keep only English/Reading Sections
df_licensedSchoolSectionsELA = \
    df_licensedSchoolSections[(df_licensedSchoolSections[3].str.contains("Reading")) | \
    (df_licensedSchoolSections[3].str.contains("English")) ]
#Create Licensed School Enrollment Dataframe
for School in LicensedSchools:
    df = df_enrollmentFile[df_enrollmentFile[4] == '320' + School]
    df_licensedSchoolEnrollments = pd.concat([df,df_licensedSchoolEnrollments])
#Keep only Enrollments that match ELA sections
df_licensedSchoolEnrollmentsELA =  \
    df_licensedSchoolEnrollments[df_licensedSchoolEnrollments[3].isin(df_licensedSchoolSectionsELA[0])]
#Drop the Column that is not Needed
df_licensedSchoolEnrollmentsELA = df_licensedSchoolSectionsELA.drop(columns=1)
#Generate Teacher Enrollments Dataframe
df_teacherELAEnrollments = df_licensedSchoolEnrollmentsELA[df_licensedSchoolEnrollmentsELA[6] == 'teacher']
df_teacherELAEnrollments = df_teacherELAEnrollments[[3, 5]]
df_teacherELAEnrollments.columns = range(df_teacherELAEnrollments.columns.size)
#Merge Teacher Enrollments into Section Dataframe
df_licensedSchoolSectionsCombined = pd.merge(df_licensedSchoolEnrollmentsELA,df_teacherELAEnrollments, how='inner')
#
df_licensedSchoolSectionsFinal['School_id'] = df_licensedSchoolSectionsCombined[9]
df_licensedSchoolSectionsFinal['Section_id'] = df_licensedSchoolSectionsCombined[0]
df_licensedSchoolSectionsFinal['TID'] = df_licensedSchoolSectionsCombined[1]
df_licensedSchoolSectionsFinal['Course_name'] = df_licensedSchoolSectionsCombined[3].rstrip(' -')
df_licensedSchoolSectionsFinal['SGRADE'] = df_licensedSchoolSectionsCombined[4]
df_licensedSchoolSectionsFinal['Course_num'] = df_licensedSchoolSectionsCombined[3].str.split(' -').str.get(1)
df_licensedSchoolSectionsFinal['Subject'] = 'ELA'
#Merge Teacher File into Section 
df_licensedSchoolSectionsFinal = df_licensedSchoolSectionsFinal.merge(df_teacherFile[['TID','TFirst','TLast']], on='TID', how='left')
########

#Freckle
df_teacherFile





# get all sections from file
# Drop non licensed schools
# Keep reading and ELA

#Create fake sections for Freckle

#Merge

