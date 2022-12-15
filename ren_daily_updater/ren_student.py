#!/usr/bin/env python3
###Renaissance Student File Script
###Script to create a file with student info
###to upload to Renaissance
###Pulls data from Active Directory
###Requires self-created module rcadinfoexport

###Import Modules###
import ldap3 as ld
import pandas as pd
import ast
import keyring
from os import getenv
from dotenv import load_dotenv
from rcadinfoexport import ad_connection #Self Created Module
from rcadinfoexport import ad_info_export #Self Created Module
#######

###Variables###
#Load Env File
load_dotenv()
#Output File
localUpFilePath = getenv('StudentUploadFile')
#AD Variables
DCServer = getenv('DCServer')
BindAccount = getenv('BindAccount')
BindServiceName = getenv('ADServiceName')
BindServiceUserName = getenv('ADServiceUserName')
BindPass = keyring.get_password(BindServiceName, BindServiceUserName)
SearchBase = getenv('StudentOU')
SearchScope = ld.SUBTREE
SearchFilter = '(&(objectCategory=person)(objectClass=user)\
    (!(userAccountControl:1.2.840.113556.1.4.803:=2)))' #Enabled Users
Attributes = getenv('StudentADAttributes').split(',')
#Spec Ed File
SpecEdFile = getenv('SpecEdFile')
#Schools with Ren Licenses
LicensedSchools = getenv('LicensedSchools').split(",")
#Empty DataFrames
df_licensedSchoolsStudents = pd.DataFrame()
df_specEdInfo = pd.DataFrame()
df_specEd = pd.DataFrame()
df_licensedSchools = pd.DataFrame()
#######

###Get Info from AD###
#Connect
DCConnection = ad_connection(DCServer,BindAccount,BindPass)
#Pull AD Data
df_ADStudentInfo = ad_info_export(DCConnection,SearchBase,Attributes,SearchScope,SearchFilter)
#Reset Index
df_ADStudentInfo.reset_index(drop=True, inplace=True)
#Drop Student Records with Missing Building
df_ADStudentInfo[Attributes[6]].replace('', 'DROP', inplace=True)
df_ADStudentInfo = df_ADStudentInfo[~df_ADStudentInfo[Attributes[6]].str.contains("DROP")]
########

###Students for Ren Licensed Schools###
for School in LicensedSchools:
    df = df_ADStudentInfo.loc[(df_ADStudentInfo[Attributes[6]] == School)]
    df_licensedSchoolsStudents = pd.concat([df_licensedSchoolsStudents, df])
#df_licensedSchoolsStudents = df_ADStudentInfo.loc[(df_ADStudentInfo[Attributes[6]] == LicensedSchool1) | \
#    (df_ADStudentInfo[Attributes[6]] == LicensedSchool2)]
########   

###Add Info to Temp Dataframes###
for pair in [(df_licensedSchools, df_licensedSchoolsStudents), \
    (df_specEd, df_ADStudentInfo)]:
    df = pair[0]
    source = pair[1]
    df['SID'] = source[Attributes[0]]
    df['SSTATEID'] = source[Attributes[0]]
    df['SFIRST'] = source[Attributes[4]]
    df['SMIDDLE'] = source[Attributes[5]]
    df['SLAST'] = source[Attributes[3]]
    df['SGRADE'] = source[Attributes[9]]
    df['SGENDER'] = source[Attributes[8]]
    df['SBIRTHDAY'] = source[Attributes[7]]
    df['RACE'] = ''
    df['SLANGUAGE'] = ''
    df['SUSERNAME'] = source[Attributes[2]]
    df['SPASSWORD'] = source[Attributes[0]]
########
				

###Spec Ed Students###
#Read Spec Ed File into Dataframe
df_specEdFile = pd.read_csv(SpecEdFile, encoding='cp1252', skiprows=1, header=None )
#Get Necessary Info for Final
df_specEdInfo['SID'] = df_specEdFile[3].astype(str)
df_specEdInfo['SID'] = df_specEdInfo['SID'].str.zfill(6)
df_specEdInfo['SCHARACTERISTICS'] = df_specEdFile[16].astype(str)
df_specEdInfo = df_specEdInfo[~df_specEdInfo['SCHARACTERISTICS'].str.contains("nan")]
#Combine Spec ED info Temp SpecEd DataFrame
df_specEd = df_specEd.merge(df_specEdInfo[['SID', 'SCHARACTERISTICS']], \
    on = 'SID', how = 'left')
#Drop
df_specEd = df_specEd[df_specEd['SCHARACTERISTICS'].notna()]
########

###Cleanup###
df_final = pd.concat([df_specEd, df_licensedSchools])
########

###Export Final File###
df_final.to_csv(localUpFilePath, index=False)
########
