### Renaissance Teacher Info Script
### Script to create a Teacher Info DataFrame
### to be Used to Generate Classlink Files 
### for Freckle

def ren_teacher_info_generator(df_users, env_file):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    from rc_google_py import download_gsheet_to_df
    #######

    ###Variables###
    #Load Env File
    load_dotenv(env_file)
    #Google Variables
    google_oauth = getenv('oauth_key')
    spec_ed_teacher_sheet = getenv('spec_ed_teacher_sheet')
    ########
    #Empty DataFrames
    df_spec_ed_check = pd.DataFrame()
    df_temp_tch_info = pd.DataFrame()
    df_spec_ed_teachers = pd.DataFrame()
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
    df_temp_tch_info['TFIRST'] = df_teachers['givenName'].str.lower()
    df_temp_tch_info['TMIDDLE'] = df_teachers['middleName']
    df_temp_tch_info['TLAST'] = df_teachers['familyName'].str.lower()
    df_temp_tch_info['TUSERNAME'] = df_teachers['email']
    df_temp_tch_info['school_id'] = df_teachers['org.sourcedId']
    ########

    ###Get Spec Ed Teacher List from Google Sheet###
    df_spec_ed_tch_sheet = download_gsheet_to_df(
                                    google_oauth, 
                                    spec_ed_teacher_sheet)
    ##Get Needed Parts for Checking
    df_spec_ed_check['TFIRST'] = df_spec_ed_tch_sheet['First Name'].str.lower()
    df_spec_ed_check['TLAST'] = df_spec_ed_tch_sheet['Last Name'].str.lower()
    df_spec_ed_check['TPOSITION'] = 'SpecEd'
    ########

    ###Create Spec ED Teacher DataFrame###
    df_spec_ed_teachers = pd.merge(df_temp_tch_info,
                        df_spec_ed_check, on=['TFIRST','TLAST'],
                        how='inner')
    ########

    ###Format Final DataFrame###
    df_spec_ed_teachers['TFIRST'] = df_spec_ed_teachers['TFIRST'].str.capitalize()
    df_spec_ed_teachers['TMIDDLE'] = df_spec_ed_teachers['TMIDDLE'].str.capitalize()
    df_spec_ed_teachers['TLAST'] = df_spec_ed_teachers['TLAST'].str.capitalize()
    df_spec_ed_teachers.drop_duplicates(inplace = True)
    ########

    return df_spec_ed_teachers

							