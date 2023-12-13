### Renaissance Freckle Class File Script
### Script to Create a File with Class info to
### Upload to Classlink for Freckle

def ren_freckle_class_generator(env_file):
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ###Variables###
    #Load Env File
    load_dotenv(env_file)
    #Course Name
    # Classlink Vars
    course_title = getenv('course_title')
    freckle_course_code = getenv('freckle_course_code')
    term_sourced_id = getenv('term_sourced_id')
    # Buildings
    building_list = getenv('building_list').split(",")
    #Empty DataFrames
    temp_dict = dict()
    df_final = pd.DataFrame()
    ####### 

    ### Freckle Classes ###
    for building in building_list:
        temp_dict['sourcedId'] = f"{building}_{freckle_course_code}"
        temp_dict['status'] = ''
        temp_dict['dateLastModified'] = ''
        temp_dict['title'] = f"{building}: {course_title}"
        temp_dict['grades'] = ''
        temp_dict['courseSourcedId'] = f"{building}_{freckle_course_code}"
        temp_dict['classCode'] = ''
        temp_dict['classType'] = 'scheduled'
        temp_dict['location'] = ''
        temp_dict['schoolSourcedId'] = building
        temp_dict['termSourcedIds'] = term_sourced_id
        temp_dict['subjects'] = 'Other'
        temp_dict['subjectCodes'] = ''
        temp_dict['periods'] = ''
        df_temp = pd.DataFrame(temp_dict, index=[building,])
        df_final = pd.concat([df_temp, df_final])
    #######

    return df_final
