### Renaissance Freckle Course File Script
### Script to Create a Course File for Freckle  
### to Upload to Classlink.  Need One per School

def ren_freckle_course_generator(env_file):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######
    
    ###Variables###
    #Load Env File
    load_dotenv(env_file)
    # Classlink Vars
    course_title = getenv('course_title')
    freckle_course_code = getenv('freckle_course_code')
    school_year_sourced_id = getenv('school_year_sourced_id')
    # Buildings
    building_list = getenv('building_list').split(",")
    #Empty DataFrames
    temp_dict = dict()
    df_final = pd.DataFrame()
    ####### 

    ### Generate Course File ###
    for building in building_list:
        temp_dict["sourcedId"] = f"{building}_{freckle_course_code}"
        temp_dict["status"] = ''
        temp_dict["dateLastModified"] = ''
        temp_dict["schoolYearSourcedId"] = school_year_sourced_id
        temp_dict["title"] = course_title
        temp_dict["courseCode"] = freckle_course_code
        temp_dict["grades"] = ''
        temp_dict["orgSourcedId"] = building
        temp_dict["subjects"] = 'Other'
        temp_dict["subjectCodes"] = ''
        df_temp = pd.DataFrame(temp_dict, index=[building,])
        df_final = pd.concat([df_temp, df_final])
    #######

    return df_final






