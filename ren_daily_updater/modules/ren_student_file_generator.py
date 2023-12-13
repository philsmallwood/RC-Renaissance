### Renaissance Student File Script: 
### Script to create a file with student info
### to upload to Renaissance

def ren_student_file_generator(df_users, df_demographics):
    ###Import Modules###
    import pandas as pd
    #######

    ###Variables###
    #Empty DataFrame
    df_spec_ed_final = pd.DataFrame()
    #######

    ### Format DataFrames ###
    # Get Students
    df_students = df_users.loc[df_users['role'].str.contains('student')].copy()
    # Convert Grade to String
    df_students['grades'] = df_students['grades'].str[0]
    # Merge Demographics into Student Info
    df_students = df_students.merge(
                                df_demographics, 
                                on = 'sourcedId', 
                                how = 'left')
    #######

    ### Spec Ed Students ###
    # Get Spec Ed Students
    df_spec_ed_students = df_students.loc[
        df_students['spec_ed'] == 'True'].copy()
    # Add to Final DataFrame
    df_spec_ed_final['SID'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['SSTATEID'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['SFIRST'] = df_spec_ed_students['givenName']
    df_spec_ed_final['SMIDDLE'] = df_spec_ed_students['middleName']
    df_spec_ed_final['SLAST'] = df_spec_ed_students['familyName']
    df_spec_ed_final['SGRADE'] = df_spec_ed_students['grades']
    df_spec_ed_final['SGENDER'] = df_spec_ed_students.sex.str[0].str.upper()
    df_spec_ed_final['SBIRTHDAY'] = pd.to_datetime(\
                                        df_spec_ed_students['birthDate']).\
                                        dt.strftime("%m/%d/%Y")
    df_spec_ed_final['RACE'] = ''
    df_spec_ed_final['SLANGUAGE'] = df_spec_ed_students['homeLanguage']
    df_spec_ed_final['SUSERNAME'] = df_spec_ed_students['email']
    df_spec_ed_final['SPASSWORD'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['school_id'] = df_spec_ed_students['primaryOrg']
    df_spec_ed_final['SCHARACTERISTICS'] = df_spec_ed_students['spec_ed']
    # Cleanup 
    df_spec_ed_final.drop_duplicates(inplace=True)
    # Format SCHARACTERISTICS
    df_spec_ed_final['SCHARACTERISTICS'] = df_spec_ed_final['SCHARACTERISTICS'].\
        str.replace('True', 'SpecEd')
    #######

    return df_spec_ed_final


