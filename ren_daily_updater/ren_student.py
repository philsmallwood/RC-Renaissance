#!/usr/bin/env python3
###Renaissance Student File Script
###Script to create a file with student info
###to upload to Renaissance

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
localUpFilePath = getenv('studentUploadFile')
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
#Empty DataFrames
df_specEdInfo = pd.DataFrame()
df_final = pd.DataFrame()
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

###Format Dataframe###
df_final['SID'] = df_ADStudentInfo[Attributes[0]]
df_final['SSTATEID'] = df_ADStudentInfo[Attributes[0]]
df_final['SFIRST'] = df_ADStudentInfo[Attributes[4]]
df_final['SMIDDLE'] = df_ADStudentInfo[Attributes[5]]
df_final['SLAST'] = df_ADStudentInfo[Attributes[3]]
df_final['SGRADE'] = df_ADStudentInfo[Attributes[9]]
df_final['SGENDER'] = df_ADStudentInfo[Attributes[8]]
df_final['SBIRTHDAY'] = df_ADStudentInfo[Attributes[7]]
df_final['RACE'] = ''
df_final['SLANGUAGE'] = ''
df_final['SUSERNAME'] = df_ADStudentInfo[Attributes[2]]
df_final['SPASSWORD'] = df_ADStudentInfo[Attributes[0]]
########					

###Add SpecEd info###
#Read Spec Ed File into Dataframe
df_specEdAll = pd.read_csv(SpecEdFile, encoding='cp1252', skiprows=1, header=None )
#Get Necessary Info for Final
df_specEdInfo['SID'] = df_specEdAll[3].astype(str)
df_specEdInfo['SID'] = df_specEdInfo['SID'].str.zfill(6)
df_specEdInfo['SCHARACTERISTICS'] = df_specEdAll[16].astype(str)
df_specEdInfo = df_specEdInfo[~df_specEdInfo['SCHARACTERISTICS'].str.contains("nan")]
#Combine Spec ED info Final
df_final = df_final.merge(df_specEdInfo[['SID', 'SCHARACTERISTICS']], \
    on = 'SID', how = 'left')
########

###Export Final File###
df_final.to_csv(localUpFilePath, index=False)
########
