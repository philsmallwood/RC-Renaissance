### Renaissance Update Main Script

### Import Modules ###
import logging
import datetime
from pathlib import Path
import pandas as pd
from modules.classlink_data_processor import ClasslinkDataProcessor
from modules.ren_student_info import ren_student_info_generator
from modules.ren_teacher_info import ren_teacher_info_generator
from modules.ren_freckle_course import ren_freckle_course_generator
from modules.ren_freckle_classes import ren_freckle_class_generator
from modules.ren_freckle_enrollments import ren_freckle_enrollments_generator
from modules.ren_sftp_uploader import sftp_upload
from google_smtp_send import google_smtp_send
from os import getenv
from dotenv import load_dotenv
#######

### Variables ###
#Env File
env_file = '.env'
#Load Env File
load_dotenv(env_file)
# API Vars
cl_api_key = getenv('cl_api_key')
cl_api_secret = getenv('cl_api_secret')
cl_api_user_url_base = getenv('cl_api_user_url_base')
cl_api_demograph_url_base = getenv('cl_api_demograph_url_base')
cl_api_items = 20000
# File Vars
ren_file_path = Path(getenv('ren_file_path'))
final_courses_file = getenv('final_courses_file')
final_classes_file = getenv('final_classes_file')
final_enrollments_file = getenv('final_enrollments_file')
upload_file_list = [final_courses_file,
                    final_classes_file,
                    final_enrollments_file]
# SFTP Vars
ren_hostname = getenv('ren_hostname')
ren_username = getenv('ren_username')
ren_key = getenv('ren_key')
# Log File
current_date = datetime.date.today()
date_str = current_date.strftime('%m-%d-%Y')
log_path = getenv('log_file_path')
log_file = f"{log_path}renaissance-updater-{date_str}.log"
# Email Alert Vars
# Email Alert Vars
alert_email = getenv('alert_email')
smtp_pass = getenv('smtp_pass')
subject = f"!!Error - Renaissance Class Upload Daily Updater Error - {date_str}!!"
#######

### Logging Setup ###
logger = logging.getLogger("ren_updater")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
    logger.addHandler(handler)
logger.propagate = False
#####################

logger.info("Renaissance Generic Class Updater Started")

### Create Classlink Connection Object ###
classlink_processor = ClasslinkDataProcessor(api_key=cl_api_key, 
                                            api_secret=cl_api_secret)
#######

### Get Classlink Data ##
try:
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
    logger.info("Data Downloaded from Classlink")
except Exception as e:
    logger.error("Classlink Data Not Downloaded")
    logger.error(e)
    raise

try:
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
    logger.info("Renaissance File Created")
except Exception as e:
    logger.error("Files not created")
    logger.error(e)
    raise


### Upload Files to Classlink ###
# Get List of Files to Upload
upload_files = [f for f in ren_file_path.iterdir() if f.is_file()]
# Upload Files
try:
    for upfile in upload_files:
        sftp_upload(ren_hostname,
                        ren_username,
                        ren_key,
                        f"{ren_file_path.name}/{upfile.name}",
                        f"{upfile.name}")
        logger.info(f"Uploaded {upfile.name} to Classlink.")
except Exception as e:
    logger.error("Files Not Uploaded to Classlink")
    logger.error(e)
    raise
#######################

### Email if Error Occurs ###
with open(log_file, "r") as f:
    if "Error" in f.read():
        google_smtp_send(alert_email,
            subject,
            smtp_pass,
            message_body=f.read())
##############################
