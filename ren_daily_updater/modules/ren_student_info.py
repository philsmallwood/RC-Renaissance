### Renaissance Student Info Script: 
### Script to Create a Student Info DataFrame
### to be Used to Generate Classlink Files 
### for Freckle

def ren_student_info_generator(df_users, df_demographics):
    ###Import Modules###
    import pandas as pd
    #######

    ###Variables###
    #Empty DataFrame
    df_final = pd.DataFrame()
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
    df_final['SID'] = df_spec_ed_students['sourcedId']
    df_final['school_id'] = df_spec_ed_students['primaryOrg']
    # Cleanup 
    df_final.drop_duplicates(inplace=True)
    #######

    return df_final


