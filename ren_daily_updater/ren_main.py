### Renaissance Update Main Script

### Import Modules ###
import pandas as pd
from modules.classlink_data_processor import ClasslinkDataProcessor
from modules.ren_student_info import ren_student_info_generator
from modules.ren_teacher_info import ren_teacher_info_generator
from modules.ren_freckle_course import ren_freckle_course_generator
from modules.ren_freckle_classes import ren_freckle_class_generator
from modules.ren_freckle_enrollments import ren_freckle_enrollments_generator
from modules.ren_sftp_uploader import ren_sftp_uploader
from os import getenv
from dotenv import load_dotenv
#######

### Variables ###
#Env File
env_file = '/config_files/env_file/.env'
#Load Env File
load_dotenv(env_file)
# API Vars
cl_api_key = getenv('cl_api_key')
cl_api_secret = getenv('cl_api_secret')
cl_api_user_url_base = getenv('cl_api_user_url_base')
cl_api_demograph_url_base = getenv('cl_api_demograph_url_base')
cl_api_items = 20000
# File Vars
final_courses_file = getenv('final_sections_file')
final_classes_file = getenv('')
final_enrollments_file = getenv('final_enrollments_file')
upload_file_list = [final_courses_file,
                    final_classes_file,
                    final_enrollments_file]
#######

### Create Classlink Connection Object ###
classlink_processor = ClasslinkDataProcessor(api_key=cl_api_key, 
                                            api_secret=cl_api_secret)
#######

### Get Classlink Data ##
# Users
## Generate User URL List
cl_api_user_url_list = classlink_processor.generate_api_url_list(
            cl_api_user_url_base, cl_api_items)
## Get User Data
df_users = classlink_processor.get_user_data(cl_api_user_url_list)
# Demographics
## Generate Demographics URL List
cl_api_demographics_url_list = classlink_processor.generate_api_url_list(
            cl_api_demograph_url_base, cl_api_items)
## Get Demographics Data
df_demographics = classlink_processor.get_demographic_data(cl_api_demographics_url_list)
#######

### Student Info ###
df_students = ren_student_info_generator(
                        df_users, 
                        df_demographics
)
#######

### Teacher Info ###
df_teachers = ren_teacher_info_generator(df_users, env_file)
#######

### Course Info ###
df_courses = ren_freckle_course_generator(env_file)
#######

### Class Info ###
df_classes = ren_freckle_class_generator(env_file)
#######

### Enrollment Info ###
df_enrollments = ren_freckle_enrollments_generator(
                        df_students,
                        df_teachers, 
                        env_file)
#######


### Export to Files ###
df_courses.to_csv(final_courses_file, index=False)
df_classes.to_csv(final_classes_file, index=False)
df_enrollments.to_csv(final_enrollments_file, index=False)
#######

### Send to Renaisance ###
ren_sftp_uploader(env_file, upload_file_list)
#######
