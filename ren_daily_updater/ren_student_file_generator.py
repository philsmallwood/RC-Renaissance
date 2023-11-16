### Renaissance Student File Script: 
### Script to create a file with student info
### to upload to Renaissance

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
    df_lic_sch_final = pd.DataFrame()
    df_spec_ed_final = pd.DataFrame()
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
    df_lic_sch_final['SID'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_lic_sch_final['SSTATEID'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_lic_sch_final['SFIRST'] = df_licensed_schools_students['givenName']
    df_lic_sch_final['SMIDDLE'] = df_licensed_schools_students['middleName']
    df_lic_sch_final['SLAST'] = df_licensed_schools_students['familyName']
    df_lic_sch_final['SGRADE'] = df_licensed_schools_students['grades']
    df_lic_sch_final['SGENDER'] = df_licensed_schools_students.sex.str[0].str.upper()
    df_lic_sch_final['SBIRTHDAY'] = pd.to_datetime(\
                                        df_licensed_schools_students['birthDate']).\
                                        dt.strftime("%m/%d/%Y")
    df_lic_sch_final['RACE'] = ''
    df_lic_sch_final['SLANGUAGE'] = df_licensed_schools_students['metadata.homeLanguage']
    df_lic_sch_final['SUSERNAME'] = df_licensed_schools_students['email']
    df_lic_sch_final['SPASSWORD'] = df_licensed_schools_students['sourcedId'].str.zfill(6)
    df_lic_sch_final['school_id'] = df_licensed_schools_students['orgSourcedIds']
    df_lic_sch_final['SCHARACTERISTICS'] = df_licensed_schools_students['metadata.spec_ed']
    #######

    ### Spec Ed Students ###
    # Get Spec Ed Students
    df_spec_ed_students = df_students.loc[
        df_students['metadata.spec_ed'] == 'True'].copy()
    # Add to Final DataFrame
    df_spec_ed_final['SID'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['SSTATEID'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['SFIRST'] = df_spec_ed_students['givenName']
    df_spec_ed_final['SMIDDLE'] = df_spec_ed_students['middleName']
    df_spec_ed_final['SLAST'] = df_spec_ed_students['familyName']
    df_spec_ed_final['SGRADE'] = df_spec_ed_students['grades']
    df_spec_ed_final['SGENDER'] = df_spec_ed_students.sex.str[0].str.upper()
    df_spec_ed_final['SBIRTHDAY'] = pd.to_datetime(\
                                        df_licensed_schools_students['birthDate']).\
                                        dt.strftime("%m/%d/%Y")
    df_spec_ed_final['RACE'] = ''
    df_spec_ed_final['SLANGUAGE'] = df_spec_ed_students['metadata.homeLanguage']
    df_spec_ed_final['SUSERNAME'] = df_spec_ed_students['email']
    df_spec_ed_final['SPASSWORD'] = df_spec_ed_students['sourcedId'].str.zfill(6)
    df_spec_ed_final['school_id'] = df_spec_ed_students['orgSourcedIds']
    df_spec_ed_final['SCHARACTERISTICS'] = df_spec_ed_students['metadata.spec_ed']
    #######

    ### Final ###
    # Combine into Final DataFrame
    df_final = pd.concat([df_lic_sch_final, df_spec_ed_final])
    # Drop Duplicates
    df_final.drop_duplicates(inplace=True)
    # Format SCHARACTERISTICS
    df_final['SCHARACTERISTICS'] = df_final['SCHARACTERISTICS'].str.replace('True', 'SpecEd')
    # Export to CSV
    df_final.to_csv(final_student_file, index=False)
    #######

    return "Renaissance Student File Generated Successfully"

if __name__ == '__main__':
    ren_student_file_generator()
    print('Renaissance Student File Generated Successfully')
