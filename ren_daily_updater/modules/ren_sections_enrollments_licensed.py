### Renaissance Section & Enrollments File Script
### Script to create two files with section and 
### enrollment info to upload to Renaissance

def ren_sec_enroll_licensed_prep(df_classes, df_enrollments):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load Env File
    load_dotenv('/config_files/env_file/.env')
    #Schools with Ren Licenses
    licensed_schools = getenv('licensed_schools').split(",")
    #Empty DataFrames
    df_licensed_school_sections = pd.DataFrame()
    df_licensed_school_enroll = pd.DataFrame()
    #######

    ### Licensed Sections/Enrollments Dataframes ###
    ## Sections
    # Create Dataframe
    for school in licensed_schools:
        df = df_classes[df_classes['school.sourcedId'] == school]
        df_licensed_school_sections = pd.concat([df,df_licensed_school_sections])
    # Get English/Reading Sections
    df_licensed_school_sec_ela = \
        df_licensed_school_sections[\
            (df_licensed_school_sections['title'].str.contains("Reading")) | \
            (df_licensed_school_sections['title'].str.contains("English")) ]
    ## Enrollment
    # Create Dataframe
    for school in licensed_schools:
        df = df_enrollments[df_enrollments['school.sourcedId'] == school]
        df_licensed_school_enroll = pd.concat([df,df_licensed_school_enroll])
    # Get ELA/Reading Enrollments
    df_licensed_school_enroll_ela =  \
        df_licensed_school_enroll[\
            df_licensed_school_enroll['class.sourcedId'].isin\
                (df_licensed_school_sec_ela['sourcedId'])]
    ########

    return df_licensed_school_sec_ela, df_licensed_school_enroll_ela 


def ren_sections_licensed(df_classes,
                        df_enrollments,
                        df_teachers):
    ###Import Modules###
    import pandas as pd
    #######

    ### Variables ###
    # Empty DataFrame
    df_licensed_school_sec_final = pd.DataFrame()
    #######

    ### Call Prep Function ### 
    df_licensed_school_sec_ela, df_licensed_school_enroll_ela = \
        ren_sec_enroll_licensed_prep(df_classes, df_enrollments)
    #######

    ### Final Licensed Section File ###
    # Generate Teacher Enrollments Dataframe
    df_ela_tch_enrolls = df_licensed_school_enroll_ela[\
                            df_licensed_school_enroll_ela['role'] == 'teacher']
    df_ela_tch_enrolls = df_ela_tch_enrolls[\
                            ['user.sourcedId', 'class.sourcedId']].copy()
    df_ela_tch_enrolls.rename(
        columns = {'class.sourcedId' : 'sourcedId' }, 
        inplace = True)
    # Merge Teacher Enrollments into Section Dataframe
    df_licensed_school_sec_combined = df_licensed_school_sec_ela.merge(\
                                    df_ela_tch_enrolls, \
                                    on='sourcedId', \
                                    how='inner')
    # Create Final Section DataFrame
    df_licensed_school_sec_final['School_id'] = df_licensed_school_sec_combined['school.sourcedId']
    df_licensed_school_sec_final['Section_id'] = df_licensed_school_sec_combined['sourcedId']
    df_licensed_school_sec_final['TID'] = df_licensed_school_sec_combined['user.sourcedId']
    df_licensed_school_sec_final['Course_name'] = df_licensed_school_sec_combined['title'].str.rstrip(' -')
    df_licensed_school_sec_final['SGRADE'] = df_licensed_school_sec_combined['grades'].str[0]
    df_licensed_school_sec_final['Course_number'] = df_licensed_school_sec_combined['title'].str.split(' -').str.get(1)
    df_licensed_school_sec_final['Subject'] = 'ELA'
    # Merge Teacher Info into Final Section DataFrame
    df_licensed_school_sec_final = df_licensed_school_sec_final.merge(\
        df_teachers[['TID','TFIRST','TLAST']], on='TID', how='left')
    ########

    return df_licensed_school_sec_final


def ren_enrollments_licensed(df_classes, df_enrollments):
    ###Import Modules###
    import pandas as pd
    #######

    ###Variables###
    # Empty DataFrames
    df_licensed_school_enroll_final = pd.DataFrame()
    #######

    ### Call Prep Function ###
    df_licensed_school_sec_ela, df_licensed_school_enroll_ela = \
        ren_sec_enroll_licensed_prep(df_classes, df_enrollments)
    #######


    ###Final Enrollment File
    #Generate Student Enrollments Dataframe
    df_student_ela_enroll = df_licensed_school_enroll_ela[\
        df_licensed_school_enroll_ela['role'] == 'student']
    #Create Final Enrollment DataFrame
    df_licensed_school_enroll_final['School_id'] = df_student_ela_enroll['school.sourcedId']
    df_licensed_school_enroll_final['Section_id'] = df_student_ela_enroll['class.sourcedId']
    df_licensed_school_enroll_final['Student_id'] = df_student_ela_enroll['user.sourcedId']
    ########

    return df_licensed_school_enroll_final
