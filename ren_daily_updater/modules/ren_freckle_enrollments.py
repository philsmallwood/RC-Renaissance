### Renaissance Freckle Enrollments File Script
### Script to Create a File with Enrollment 
### Info to Upload to Classlink for Freckle

def ren_freckle_enrollments_generator(df_students,
                                    df_teachers,
                                    env_file) :
    ### Import Modules ###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    #######

    ### Variables ###
    #Load Env File
    load_dotenv(env_file)
    # Classlink Vars
    freckle_course_code = getenv('freckle_course_code')
    #Empty DataFrames
    df_student_enroll = pd.DataFrame()
    df_teacher_enroll = pd.DataFrame()
    #######

    ### Student Freckle Enrollments ###
    df_student_enroll['sourcedId'] = df_students['school_id'] + f"_{freckle_course_code}_S" + df_students['SID'] 
    df_student_enroll['status'] = ''
    df_student_enroll['dateLastModified'] = '' 
    df_student_enroll['classSourcedId'] = df_students['school_id'] + f"_{freckle_course_code}"
    df_student_enroll['schoolSourcedId'] = df_students['school_id']
    df_student_enroll['userSourcedId'] = df_students['SID']
    df_student_enroll['role'] = 'student'
    df_student_enroll['primary'] = ''
    df_student_enroll['beginDate'] = '2023-07-03'
    df_student_enroll['endDate'] = '2024-06-11'
    #######

    ### Teacher Freckle Enrollments ###
    df_teacher_enroll['sourcedId'] = df_teachers['school_id'] + f"_{freckle_course_code}_T" + df_teachers['TID'] 
    df_teacher_enroll['status'] = ''
    df_teacher_enroll['dateLastModified'] = '' 
    df_teacher_enroll['classSourcedId'] = df_teachers['school_id'] + f"_{freckle_course_code}"
    df_teacher_enroll['schoolSourcedId'] = df_teachers['school_id']
    df_teacher_enroll['userSourcedId'] = df_teachers['TID']
    df_teacher_enroll['role'] = 'teacher'
    df_teacher_enroll['primary'] = ''
    df_teacher_enroll['beginDate'] = '2023-07-03'
    df_teacher_enroll['endDate'] = '2024-06-11'
    #######

    ### Combine Teacher and Student Enrollments ###
    df_final = pd.concat([df_student_enroll, df_teacher_enroll])
    #######
    
    return df_final
