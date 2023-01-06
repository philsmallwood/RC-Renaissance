#!/usr/bin/env python3
###Renaissance Freckle Section & Enrollments File Script
###Script to create two files with section and 
###enrollment info to upload to Renaissance
###for the Freckle sections
###Requires exported user file from Classlink

###Import Modules###
import pandas as pd
from os import getenv
from dotenv import load_dotenv
#######

###Variables###
#Load Env File
load_dotenv()
#Output File
FreckleSectionFile = getenv('FreckleSectionUploadFile')
FreckleEnrollmentFile = getenv('FreckleEnrollmentUploadFile')
#Data Files
classlinkStudentFile = getenv('StudentUploadFile')
classlinkTeacherFile = getenv('TeacherUploadFile')
LicensedSectionFile = getenv('LicensedSectionUploadFile')
LicensedEnrollmentFile = getenv('LicensedEnrollmentUploadFile')
#Course Name
courseName = getenv('courseName')
#Empty DataFrames
df_specialSections = pd.DataFrame()
df_specialEnrollments = pd.DataFrame()
#######

###Freckle Sections###
#Read Renaissance Teacher File 
df_teacherFile = pd.read_csv(classlinkTeacherFile, dtype=str)
#Get SpecED Teachers
df_specEdTeachers = df_teacherFile.loc[df_teacherFile['TPOSITION'] == 'SpecEd']
#Format Section Dataframe for Freckle Sections
df_specialSections['School_id'] = df_specEdTeachers['school_id']
df_specialSections['Section_id'] = df_specEdTeachers['school_id'] + '-' + courseName
df_specialSections['TID'] = df_specEdTeachers['TID']
df_specialSections['TFirst'] = df_specEdTeachers['TFIRST']
df_specialSections['TLast'] = df_specEdTeachers['TLAST']
df_specialSections['Course_name'] = courseName
df_specialSections['Course_number'] = '3299999'
df_specialSections['Subject'] = 'Other'
#######

###Freckle Enrollments###
#Read Renaissance Student File
df_studentFile = pd.read_csv(classlinkStudentFile, dtype=str)
#Get SpecEd Students
df_specEdStudents =  df_studentFile[df_studentFile['SCHARACTERISTICS'].notnull()]
#Format Enrollment Dataframe for Freckle Sections
df_specialEnrollments['School_id'] = df_specEdStudents['school_id']
df_specialEnrollments['Section_id'] = df_specEdStudents['school_id'] + '-' + courseName
df_specialEnrollments['Student_id'] = df_specEdStudents['SID']
#######

###Add Freckle Information to Licensed Information###
#Read Renaissance Licensed Section 
#and Enrollment Files into DataFrames
df_licensedSchoolSections = pd.read_csv(LicensedSectionFile, dtype=str)
df_licensedSchoolEnrollments = pd.read_csv(LicensedEnrollmentFile, dtype=str)
#Combine Freckle DataFrames into Licensed DataFrames
df_mergedSections = pd.concat([df_specialSections,df_licensedSchoolSections])
df_mergedEnrollments = pd.concat([df_specialEnrollments,df_licensedSchoolEnrollments])
#######

###Export Final Files###
df_mergedSections.to_csv(LicensedSectionFile, index=False)
df_mergedEnrollments.to_csv(LicensedEnrollmentFile, index=False)
########

