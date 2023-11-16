### Renaissance Student File Script: 
### Script to create a file with student info
### to upload to Renaissance
### Pulls data from Active Directory
### Requires self-created module rcadinfoexport

def ren_student_file_generator():
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load Env File
    load_dotenv()
    #Output File
    final_student_file = getenv('final_student_file')
    #Student Info File
    user_file = getenv('user_file')
    demographic_file = getenv('demographics_file')
    #Schools with Ren Licenses
    licensed_schools = getenv('licensed_schools').split(",")
    #Empty DataFrames
    df_licensed_schools_students = pd.DataFrame()
    df_final = pd.DataFrame()
    #######

    ### Read Files to DataFrames ###
    # User File
    df_users = pd.read_csv(user_file, 
                        dtype = str)
    # Demographic File
    df_demographics = pd.read_csv(demographic_file, 
                                dtype = str)
    #######

    ### Format DataFrames ###
    # Get Students
    df_students = df_users.loc[df_users['role'].str.contains('student')].copy()
    # Merge Demographics into Student Info
    df_students = df_students.merge(
                                df_demographics, 
                                on = 'sourcedId', 
                                how = 'left')
    #######

    ### Licensed Schools ###
    # Get Licensed Schools
    for school in licensed_schools:
        df = df_students.loc[df_students['orgSourcedIds'] == school].copy()
        df_licensed_schools_students = pd.concat([df_licensed_schools_students, df])
    # Add to Final DataFrame
    df_final['SID'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_final['SSTATEID'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_final['SFIRST'] = df_licensed_schools_students['givenName']
    df_final['SMIDDLE'] = df_licensed_schools_students['middleName']
    df_final['SLAST'] = df_licensed_schools_students['familyName']
    df_final['SGRADE'] = df_licensed_schools_students['grades']
    df_final['SGENDER'] = df_licensed_schools_students.sex.str[0].str.upper()
    df_final['SBIRTHDAY'] = pd.to_datetime(\
                                        df_licensed_schools_students['birthDate']).\
                                        dt.strftime("%m/%d/%Y")
    df_final['RACE'] = ''
    df_final['SLANGUAGE'] = df_licensed_schools_students['metadata.homeLanguage']
    df_final['SUSERNAME'] = df_licensed_schools_students['email']
    df_final['SPASSWORD'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_final['school_id'] = df_licensed_schools_students['sourcedId']
    #######

    ### Spec Ed Students ###
    df_spec_ed_students = df_students.loc[
        df_students['metadata.spec_ed'] == 'True']
