### Renaissance Freckle Section & Enrollments File Script
### Script to create two files with section and 
### enrollment info to upload to Renaissance
### for the Freckle sections

def ren_sections_special(df_teachers):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load Env File
    load_dotenv('/config_files/env_file/.env')
    #Course Name
    courseName = getenv('courseName')
    #Empty DataFrames
    df_special_sections = pd.DataFrame()
    #######

    ### Freckle Sections ###
    # Get SpecED Teachers
    df_spec_ed_teachers = df_teachers.loc[df_teachers['TPOSITION'] == 'SpecEd']
    #Format Section Dataframe for Freckle Sections
    df_special_sections['School_id'] = df_spec_ed_teachers['school_id']
    df_special_sections['Section_id'] = df_spec_ed_teachers['school_id'] + '-' + courseName
    df_special_sections['TID'] = df_spec_ed_teachers['TID']
    df_special_sections['TFirst'] = df_spec_ed_teachers['TFIRST']
    df_special_sections['TLast'] = df_spec_ed_teachers['TLAST']
    df_special_sections['Course_name'] = courseName
    df_special_sections['Course_number'] = '3299999'
    df_special_sections['Subject'] = 'Other'
    #######

    return df_special_sections
############################################

def ren_enrollments_special(df_students):
    ### Import Modules ###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ### Variables ###
    #Load Env File
    load_dotenv('/config_files/env_file/.env')
    #Course Name
    courseName = getenv('courseName')
    #Empty DataFrames
    df_special_enrollments = pd.DataFrame()
    #######

    ### Freckle Enrollments ###
    #Get SpecEd Students
    df_spec_ed_students =  df_students[df_students['SCHARACTERISTICS'].notnull()]
    #Format Enrollment Dataframe for Freckle Sections
    df_special_enrollments['School_id'] = df_spec_ed_students['school_id']
    df_special_enrollments['Section_id'] = df_spec_ed_students['school_id'] + '-' + courseName
    df_special_enrollments['Student_id'] = df_spec_ed_students['SID']
    #######

    return df_special_enrollments
