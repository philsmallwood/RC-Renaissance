### Renaissance Update Main Script

### Import Modules ###
import pandas as pd
from modules.classlink_data_processor import ClasslinkDataProcessor
from modules.ren_student_file_generator import ren_student_file_generator
from modules.ren_teacher_file_generator import ren_teacher_file_generator
from modules.ren_sections_enrollments_special import ren_sections_special, ren_enrollments_special
from modules.ren_sections_enrollments_licensed import ren_sections_licensed, ren_enrollments_licensed
from modules.ren_sftp_uploader import ren_sftp_uploader
from os import getenv
from dotenv import load_dotenv
#######

### Variables ###
#Load Env File
load_dotenv('/config_files/env_file/.env')
# API Vars
cl_api_key = getenv('cl_api_key')
cl_api_secret = getenv('cl_api_secret')
cl_api_user_url_base = getenv('cl_api_user_url_base')
cl_api_demograph_url_base = getenv('cl_api_demograph_url_base')
cl_api_classes_url_base = getenv('cl_api_classes_url_base')
cl_api_enroll_url_base = getenv('cl_api_enroll_url_base')
cl_api_items = 20000
cl_api_items_lrg = cl_api_items * 10
# File Vars
final_student_file = getenv('final_student_file')
final_teacher_file = getenv('final_teacher_file')
final_sections_file = getenv('final_sections_file')
final_enrollments_file = getenv('final_enrollments_file')
upload_file_list = [final_student_file,
                    final_teacher_file,
                    final_sections_file,
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
# Classes
## Generate Classes URL List
cl_api_classes_url_list = classlink_processor.generate_api_url_list(
            cl_api_classes_url_base, cl_api_items)
## Get Classes Data
df_classes = classlink_processor.get_class_data(cl_api_classes_url_list)
# Enrollments
## Generate Enrollments URL List
cl_api_enroll_url_list = classlink_processor.generate_api_url_list(
            cl_api_enroll_url_base, cl_api_items_lrg)
## Get Enrollments Data
df_enrollments = classlink_processor.\
                        get_enrollment_data(\
                            cl_api_enroll_url_list)
#######

### Student.Csv File ###
df_students = ren_student_file_generator(
                        df_users, 
                        df_demographics
)
#######

### Teachers.csv ###
df_teachers = ren_teacher_file_generator(df_users)
#######

### Sections/Enrollment ###
# Spec Ed Sections
df_spec_ed_sections = ren_sections_special(df_teachers)
# Spec Ed Enrollments
df_spec_ed_enrollments = ren_enrollments_special(df_students)
# Licensed Schools Sections
df_licensed_sections = ren_sections_licensed(
        df_classes, 
        df_enrollments, 
        df_teachers)
# Licensed Schools Enrollments
df_licensed_enrollments = ren_enrollments_licensed(
        df_classes, 
        df_enrollments)
# Combined Sections
df_sections_combined = pd.concat([df_spec_ed_sections, df_licensed_sections])
# Combined Enrollments
df_enrollments_combined = pd.concat([df_spec_ed_enrollments, 
                                    df_licensed_enrollments])
#######

### Export to Files ###
df_students.to_csv(final_student_file, index=False)
df_teachers.to_csv(final_teacher_file, index=False)
df_sections_combined.to_csv(final_sections_file, index=False)
df_enrollments_combined.to_csv(final_enrollments_file, index=False)
#######

### Send to Renaisance ###
ren_sftp_uploader(upload_file_list)
#######
