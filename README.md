# RC-Renaissance

### Scripts to Work with Renaissance

### Repo: RC-Renaissance
### Languages: Python

##### Ren Daily Updater

The Renaissance Update process involves a set of Python scripts for managing data related to Renaissance Learning. The main script, ren_main.py, orchestrates the entire process. Here's an overview of each script's functionality:

1. Renaissance Update Main Script (ren_main.py):

+ Imports necessary modules, including Pandas and dotenv.
+ Retrieves data from Classlink API, processes it, and generates CSV files for students, teachers, sections, and enrollments.
+ Utilizes a ClasslinkDataProcessor class for handling API requests and data extraction.
+ Sends the generated files to 

2. Renaissance via SFTP.
ClasslinkDataProcessor (classlink_data_processor.py):

+ Handles authentication and requests to the Classlink API.
+ Retrieves user, demographic, class, and enrollment data from Classlink.
+ Generates API URLs based on specified parameters.

3. OneRoster (oneroster.py):

+ Implements OAuth1 authentication for making requests to a given URL.
+ Generates the OAuth signature for secure communication with the OneRoster API.

4. Renaissance Student File Script (ren_student_file_generator.py):

+ Generates a file containing student information for uploading to Renaissance.
+ Processes data from Classlink, filters students, and formats the file with required fields.

5. Renaissance Teacher File Script (ren_teacher_file_generator.py):

+ Creates a file with teacher information for Renaissance upload.
+ Retrieves teacher data from Classlink, filters and formats the file with necessary fields.

6. Renaissance Freckle Section & Enrollments File Script (ren_sections_enrollments_special.py):

+ Generates two files with section and enrollment info for Freckle sections.
+ Creates separate DataFrames for special education sections and enrollments.

7. Renaissance Section & Enrollments File Script (ren_sections_enrollments_licensed.py):

+ Creates two files with section and enrollment info for Renaissance.
+ Prepares licensed school sections and enrollments, including English/Reading sections.

8. Renaissance File Uploader (ren_sftp_uploader.py):

+ Uploads files to the Renaissance SFTP server using PySFTP.
+ Retrieves SFTP connection details from environment variables.

Scripts need a configured .env file in the same path.   