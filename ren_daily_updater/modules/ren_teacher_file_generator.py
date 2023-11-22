### Renaissance Teacher File Script
### Script to create a file with teacher info
### to upload to Renaissance

def ren_teacher_file_generator(df_users):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    from rc_google_py import download_gsheet_to_df
    #######

    ###Variables###
    #Load Env File
    load_dotenv('/config_files/env_file')
    #Schools with Ren Licenses
    licensed_schools = getenv('licensed_schools').split(",")
    #Google Variables
    google_oauth = getenv('oauth_key')
    spec_ed_teacher_sheet = getenv('spec_ed_teacher_sheet')
    ########
    #Empty DataFrames
    df_spec_ed_check = pd.DataFrame()
    df_temp_tch_info = pd.DataFrame()
    df_licensed_schools = pd.DataFrame()
    df_final = pd.DataFrame()
    #######

    ### Read Files to DataFrames ###
    # Get Teachers
    df_teachers = df_users.loc[\
                (df_users['role'].str.contains('teacher')) |\
                (df_users['role'].str.contains('aide'))].copy()
    # Drop 'Fake' Accounts
    df_teachers = df_teachers[~df_teachers['email'].str.contains("test")]
    ########

    ###Format Temp Dataframe###
    df_temp_tch_info['TID'] = df_teachers['sourcedId']
    df_temp_tch_info['TSTATEID'] = ''
    df_temp_tch_info['TFIRST'] = df_teachers['givenName'].str.lower()
    df_temp_tch_info['TMIDDLE'] = df_teachers['middleName']
    df_temp_tch_info['TLAST'] = df_teachers['familyName'].str.lower()
    df_temp_tch_info['TGENDER'] = ''
    df_temp_tch_info['TUSERNAME'] = df_teachers['email']
    df_temp_tch_info['PASSWORD'] = getenv('fake_pass')
    df_temp_tch_info['school_id'] = df_teachers['primaryOrg']
    ########

    ###Get Spec Ed Teacher List from Google Sheet###
    df_spec_ed_tch_sheet = download_gsheet_to_df(
                                    google_oauth, 
                                    spec_ed_teacher_sheet)
    ##Get Needed Parts for Checking
    df_spec_ed_check['TFIRST'] = df_spec_ed_tch_sheet['First Name'].str.lower()
    df_spec_ed_check['TLAST'] = df_spec_ed_tch_sheet['Last Name'].str.lower()
    df_spec_ed_check['TPOSITION'] = 'SpecEd'
    df_spec_ed_check['school_id'] = df_spec_ed_tch_sheet['school_id'].astype(str)
    ########

    ###Create Spec ED Teacher DataFrame###
    df_spec_ed = pd.merge(df_temp_tch_info,
                        df_spec_ed_check, 
                        how='inner')
    ########

    ###Create Licensed School Teacher DataFrame###
    for school in licensed_schools:
        df = df_temp_tch_info.loc[(df_temp_tch_info['school_id'] == school)]
        df_licensed_schools = pd.concat([df,df_licensed_schools])
    ########

    ###Format Final DataFrame###
    df_final = pd.concat([df_spec_ed, df_licensed_schools])
    df_final['TFIRST'] = df_final['TFIRST'].str.capitalize()
    df_final['TMIDDLE'] = df_final['TMIDDLE'].str.capitalize()
    df_final['TLAST'] = df_final['TLAST'].str.capitalize()
    df_final.drop_duplicates(inplace = True)
    ########

    return df_final

							